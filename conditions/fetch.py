import requests, json

def get_weather_data(city_name):
    api_key = "82f0629226863f638585e84561e00e1d"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key

    response = requests.get(complete_url)

    x = response.json()
    list = x["list"]
    data = list[0]


    response_data = {}

    if x["cod"] != "404":
        response_data['temp'] = data["main"]["temp"]
        response_data['windspeed'] = data["wind"]['speed']
        response_data['degree'] = data["wind"]["deg"]

        response_data['visibility'] = data["visibility"]
        response_data['clouds'] = data["clouds"]['all']
        response_data['rain_probability'] = data["rain"]["3h"]
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
    cleaned_response["rain_probability"] = response.get("rain_probability")

    return cleaned_response

def kelvin_to_fahrenheit(temp):
    new_temp = ((temp - 273.15) * (9.0/5.0)) + 32
    return new_temp

def mph_to_knots(speed):
    return speed * .868976


def meters_to_statute_meters(meters):
    return meters * .00062137119223733
