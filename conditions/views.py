from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from django.db.models import Count

from .fetch import get_weather_data, convert_data, kelvin_to_fahrenheit, meters_to_statute_meters
from .models import City

def are_conditions_met(data):
    counter = 0
    if data["visibility"] >= 10.0:
        counter += 1
    if data["windspeed"] < 30.0:
        counter += 1
    if data["temp"] > 32.0 and data["temp"] < 90:
        counter += 1
    if data['weather'].substring("snow") == -1  and data['weather'].substring('rain') == -1:
        counter += 1
    if data['description'].substring("snow") == -1 and data['description'].substring('rain') == -1 and data['description'].substring('ice') == -1:
        counter += 1
    return counter == 5

def view_conditions(request):
    #requested_city = get_object_or_404(City, pk=city_pk)
    requested_city = "Columbus"

    weather_data = convert_data(get_weather_data(requested_city))
    weather_data['are_conditions_met'] = are_conditions_met(weather_data)

    return render(request, 'conditions.html', weather_data)

def view_cities(request):
    return render(request, 'view_cities.html')
