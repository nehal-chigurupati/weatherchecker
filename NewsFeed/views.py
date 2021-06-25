from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import requests
import time as time
import nltk

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
