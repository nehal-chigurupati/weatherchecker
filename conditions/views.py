from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from django.db.models import Count

from .fetch import get_weather_data, convert_data, kelvin_to_fahrenheit, meters_to_statute_meters
from .fetch import getActiveFlightsToAirport, getActiveFlightsFromAirport
from .models import City
from .IATA_CODES import IATA_CODES

def are_conditions_met(data):
    counter = 0
    if data["visibility"] >= 6:
        counter += 1
    if data["windspeed"] < 30.0:
        counter += 1
    if data["temp"] > 32.0 and data["temp"] < 90:
        counter += 1
    if data['weather'].find("snow") == -1  and data['weather'].find('rain') == -1:
        counter += 1
    if data['description'].find("snow") == -1 and data['description'].find('ice') == -1:
        counter += 1
    else:
        print("test 5 failed")
    return counter == 5

def home(request):
    available_cities = City.objects.all()
    is_safe_for_flying = {}
    for city in City.objects.all():
        is_safe_for_flying[city.get_fetchable_name] = are_conditions_met(convert_data(get_weather_data(city.get_fetchable_name())))

    return render(request, 'home.html', {'available_cities': available_cities})



def view_conditions(request, pk):
    city_object = get_object_or_404(City, pk=pk)
    requested_city = city_object.get_fetchable_name()

    weather_data = convert_data(get_weather_data(requested_city))
    flights_to_airport = getActiveFlightsToAirport(IATA_CODES[requested_city])
    flights_from_airport = getActiveFlightsFromAirport(IATA_CODES[requested_city])
    weather_data['are_conditions_met'] = are_conditions_met(weather_data)
    weather_data['city'] = requested_city
    

    return render(request, 'conditions.html', {'weather': weather_data, 'flights_to_airport': flights_to_airport, 'flights_from_airport': flights_from_airport})

def view_cities(request):
    return render(request, 'view_cities.html')
