from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import LocationCoordinates, WikiPage
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import requests
import time as time
import nltk
import os
import wikipediaapi

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

from nltk.corpus import stopwords

"""
NEWSAPI.ORG API KEY:
4f6aaa0c97e54580b9c97be06dc24468
"""


class NewsAPI:

    class Everything:
        def fetch(**kwargs):
            """
            params explanation at following URL:
            https://newsapi.org/docs/endpoints/everything
            """

            kwargs['apiKey'] = '4f6aaa0c97e54580b9c97be06dc24468'
            data = requests.get('https://newsapi.org/v2/everything', params=kwargs)
            return data.json()

    class TopHeadlines:
        def fetch(**kwargs):
            """
            params explanation at following URL:
            https://newsapi.org/docs/endpoints/everything
            """
            kwargs['apiKey'] = '4f6aaa0c97e54580b9c97be06dc24468'
            data = requests.get('https://newsapi.org/v2/top-headlines', params=kwargs)
            return data.json()

    class Source:
        def fetch(**kwargs):
            """
            params explanation at following URL:
            https://newsapi.org/docs/endpoints/sources
            """

            kwargs['apiKey'] = '4f6aaa0c97e54580b9c97be06dc24468'
            data = requests.get('https://newsapi.org/v2/sources', params=kwargs)
            return data.json()

    def GetHeadlines():
        all_top_headlines = NewsAPI.TopHeadlines.fetch(language='en')
        articles = all_top_headlines['articles']
        headlines = []
        for item in articles:
            headlines.append(item['title'])
        return headlines

    def GetHeadlineLinks():
        all_top_headlines = NewsAPI.TopHeadlines.fetch(language='en')
        articles = all_top_headlines['articles']
        headlines = []
        for item in articles:
            headlines.append(item['url'])
        return headlines


def GetNouns(inputString):
    words = nltk.word_tokenize(inputString)
    stop_words = set(stopwords.words("english"))

    filtered_list = []

    for word in words:
        if word.casefold() not in stop_words:
            filtered_list.append(word)

    tagged_words = []
    noun_tags = ['NN', 'NNP', 'NNPS', 'NNS']
    tokenized_words = nltk.pos_tag(filtered_list)

    for item in tokenized_words:
        listified_item = list(item)
        if listified_item[1] in noun_tags:
            tagged_words.append(listified_item[0])
    return tagged_words

def GetProperNouns(inputString):
    nouns = GetNouns(inputString)
    proper_nouns = ['NNP', 'NNPS']
    tokenized_words = nltk.pos_tag(nouns)
    tagged_words = []
    for item in tokenized_words:
        listified_item = list(item)
        if listified_item[1] in proper_nouns:
            tagged_words.append(listified_item[0])
    return tagged_words

def GetVerbs(inputString):
        words = nltk.word_tokenize(inputString)
        stop_words = set(stopwords.words("english"))

        filtered_list = []

        for word in words:
            if word.casefold() not in stop_words:
                filtered_list.append(word)

        tagged_words = []
        verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

        tokenized_words = nltk.pos_tag(filtered_list)

        for item in tokenized_words:
            listified_item = list(item)
            if listified_item[1] in verb_tags:
                tagged_words.append(listified_item[0])
        return tagged_words

def GetKeywords():
    all_headlines = NewsAPI.GetHeadlines()
    keywords = []
    for item in all_headlines:
        keywords.append(GetProperNouns(item))

    return keywords


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetHeadlines(request):
    data = request.data
    if request.method == 'GET':
        all_headlines = NewsAPI.GetHeadlines()
        all_links = NewsAPI.GetHeadlineLinks()
        headline_dict = {}
        all_keywords = GetKeywords()
        counter = 0
        for item in all_headlines:
            keywords = all_keywords[counter]
            headline_dict[item] = {'keywords': keywords, 'URL': all_links[counter]}
            counter += 1

        return Response(headline_dict)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def Locations(request):
    data = request.data
    if request.method == 'POST':
        location_stamp = LocationCoordinates(coordinates=data['coordinates'])
        location_stamp.save()
        return Response(status=201)
    elif request.method == 'GET':
        ResponseDict = {}
        all_coordinates = list(LocationCoordinates.objects.all())
        for location in all_coordinates:
            ResponseDict[location.GetTime()] = location.GetCoordinates()

        return Response(ResponseDict)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Wiki(request):
    """
    TO FETCH FROM WIKI, PUT THINGS IN PARAMS ARG IN REQUESTS LIB PYTHON
    """
    data = request.query_params
    if request.method == 'GET':
        search_term = data['search_term']
        print(search_term)
        all_pages = list(WikiPage.objects.all())
        return_text = ""

        search_results = WikiPage.objects.filter(search_term=search_term)
        if len(search_results) == 0:
            wiki = wikipediaapi.Wikipedia('en')
            page = wiki.page(search_term)
            new_saved_page = WikiPage(search_term=search_term, text=page.text)
            new_saved_page.save()
            return Response({'text': page.text})
        elif len(search_results) == 1:
            page = list(search_results)[0]
            return Response({'text': page.text})

class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
