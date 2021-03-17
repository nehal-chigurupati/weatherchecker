import requests, json
import time as time

def getActiveFlightsToAirport(arriving_airport_iata):
    params = {
        'access_key': 'a1c8611fb0c9eead98c3792c15f2e1cc',
        'arr_iata': arriving_airport_iata,
        'flight_status': 'active'
    }

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    timeOfFetch = time.time()

    api_response = api_result.json()
    data = api_response['data']
    departing_dict = {}


    for flight in data:
        #flight Number
        if flight['flight'] != None:
            flightNumber = flight['flight']['iata']
        else:
            flightNumber = None

        #flight aircraft
        if flight['aircraft'] != None:
            flightRegistration = flight['aircraft']['registration']
        else:
            flightRegistration = None

        #flight departure
        if flight['departure'] != None:
            flightDeparture = flight['departure']['airport']
        else:
            flightDeparture = None

        #estimated arrival
        if flight['arrival'] != None:
            flightEstimatedArrival = flight['arrival']['estimated']
        else:
            flightEstimatedArrival = None

        #current latitude, longitude, horizontal, vertical speeds and altitude
        if flight['live'] != None:
            flightLatitude = flight['live']['latitude']
            flightLongitude = flight['live']['longitude']
            flightAltitude = flight['live']['altitude']
            flightDirection = flight['live']['direction']
            flightSpeedHorizontal = flight['live']['speed_horizontal']
            flightSpeedVertical = flight['live']['speed_vertical']
        else:
            flightLatitude = None
            flightLongitude = None
            flightAltitude = None
            flightDirection = None
            flightSpeedHorizontal = None
            flightSpeedVertical = None

        departing_dict[flightNumber] = {'flightNumber': flightNumber, 'flightRegistration': flightRegistration, 'flightDeparture': flightDeparture, 'flightDestination': arriving_airport_iata,
            'flightEstimatedArrival': flightEstimatedArrival, 'flightLatitude': flightLatitude, 'flightLongitude': flightLongitude,
            'flightAltitude': flightAltitude, 'flightDirection': flightDirection, 'flightSpeedHorizontal': flightSpeedHorizontal,
            'flightSpeedVertical': flightSpeedVertical}
    processingTime = time.time() - timeOfFetch
    departing_dict['processingTime'] = time.time()
    departing_dict['timeOfFetch'] = timeOfFetch

    return departing_dict

def getActiveFlightsFromAirport(departing_airport_iata):
    params = {
        'access_key': 'a1c8611fb0c9eead98c3792c15f2e1cc',
        'dep_iata': departing_airport_iata,
        'flight_status': 'active'
    }

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    timeOfFetch = time.time()

    api_response = api_result.json()
    data = api_response['data']
    departing_dict = {}


    for flight in data:
        #flight Number
        if flight['flight'] != None:
            flightNumber = flight['flight']['iata']
        else:
            flightNumber = None

        #flight aircraft
        if flight['aircraft'] != None:
            flightRegistration = flight['aircraft']['registration']
        else:
            flightRegistration = None

        #flight destination
        if flight['arrival'] != None:
            flightDestination = flight['arrival']['airport']
        else:
            flightDestination = None

        #estimated arrival
        if flight['arrival'] != None:
            flightEstimatedArrival = flight['arrival']['estimated']
        else:
            flightEstimatedArrival = None

        #current latitude, longitude, horizontal, vertical speeds and altitude
        if flight['live'] != None:
            flightLatitude = flight['live']['latitude']
            flightLongitude = flight['live']['longitude']
            flightAltitude = flight['live']['altitude']
            flightDirection = flight['live']['direction']
            flightSpeedHorizontal = flight['live']['speed_horizontal']
            flightSpeedVertical = flight['live']['speed_vertical']
        else:
            flightLatitude = None
            flightLongitude = None
            flightAltitude = None
            flightDirection = None
            flightSpeedHorizontal = None
            flightSpeedVertical = None

        departing_dict[flightNumber] = {'flightNumber': flightNumber, 'flightRegistration': flightRegistration, 'flightDestination': flightDestination, 'flightDeparture': departing_airport_iata,
            'flightEstimatedArrival': flightEstimatedArrival, 'flightLatitude': flightLatitude, 'flightLongitude': flightLongitude,
            'flightAltitude': flightAltitude, 'flightDirection': flightDirection, 'flightSpeedHorizontal': flightSpeedHorizontal,
            'flightSpeedVertical': flightSpeedVertical}
    processingTime = time.time() - timeOfFetch
    departing_dict['processingTime'] = time.time()
    departing_dict['timeOfFetch'] = timeOfFetch

    return departing_dict

def get_weather_data(city_name):
    api_key = "82f0629226863f638585e84561e00e1d"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key

    response = requests.get(complete_url)

    x = response.json()
    list = x["list"]
    data = list[1]


    response_data = {}

    if x["cod"] != "404":
        response_data['temp'] = data["main"]["temp"]
        response_data['windspeed'] = data["wind"]['speed']
        response_data['degree'] = data["wind"]["deg"]

        response_data['visibility'] = data["visibility"]
        response_data['clouds'] = data["clouds"]['all']
        response_data['weather'] = data["weather"][0]["main"]
        response_data['description'] = data['weather'][0]["description"]
    else:
        response_data["ERROR"] = "ERROR IN FETCH"
    return response_data

def convert_data(response):
    cleaned_response = {}
    cleaned_response['temp'] = kelvin_to_fahrenheit(response.get("temp"))
    cleaned_response['windspeed'] = mph_to_knots(response.get("windspeed"))
    cleaned_response["degree"] = response.get("degree")
    cleaned_response["visibility"] = meters_to_statute_meters(response.get("visibility"))
    cleaned_response["clouds"] = response.get("clouds")
    cleaned_response["weather"] = response.get("weather")
    cleaned_response["description"] = response.get("description")

    return cleaned_response

def kelvin_to_fahrenheit(temp):
    new_temp = ((temp - 273.15) * (9.0/5.0)) + 32
    return new_temp

def mph_to_knots(speed):
    return speed * .868976


def meters_to_statute_meters(meters):
    return meters * .00062137119223733
