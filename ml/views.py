from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ml.TrainingEngine.Executor import *

from sklearn import tree
import numpy as np

import pickle

def GetInputArray(origin, destination, carrier):
    AirportsEncodingDict = pickle.load(open('ml/FlightDelayFiles/encodingDictAirportsTreeModel1.pkl', 'rb'))
    CarriersEncodingDict = pickle.load(open('ml/FlightDelayFiles/encodingDictCarriersTreeModel1.pkl', 'rb'))

    origin = AirportsEncodingDict[origin]
    destination = AirportsEncodingDict[destination]
    carrier = CarriersEncodingDict[carrier]
    data = np.array([np.array([origin, destination, carrier])])

    return data

@api_view(['GET'])
def FlightDelayPrediction(request):
    RequestInfo = request.query_params
    if 'origin' in RequestInfo and 'destination' in RequestInfo and 'carrier' in RequestInfo:
        data = GetInputArray(RequestInfo['origin'], RequestInfo['destination'], RequestInfo['carrier'])
        prediction = 0
        model = pickle.load(open('ml/FlightDelayFiles/FlightDelayTreeClassifier.pkl', 'rb'))
        prediction = model.predict(data)
        return Response({'might_be_delayed': (prediction == 1)[0]}, template_name='flightdelayprediction.html')
    else:
        return render(request, 'flightdelayprediction.html')

@api_view(['GET'])
def ModelEngine(request):
    RequestInfo = request.query_params
    if 'sequence' in RequestInfo:
        sequence = RequestInfo['sequence']
        current_executor = Executor(sequence)
        return Response(current_executor.parse())
    else:
        return render(request, 'modelengine.html')

@api_view(['POST','GET'])
def WriteCode(request):
    if request.method == 'POST':
        data = request.data
        f = open("ml/CodeFiles/" + data['filename'], "a")
        f.write(data['code'])
        f.close()
        return Response(status=201)
    else:
        params = request.query_params
        f = open("ml/CodeFiles/" + params['filename'], "r")
        contents = f.read()
        f.close()
        return Response({'contents': contents})
