import openmeteo_requests
from geopy.geocoders import Nominatim

def getlat(place: str):
    geolocator = Nominatim(user_agent="goofygobers12345")
    location = geolocator.geocode(place)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return longitude, latitude
    else:
        raise ValueError(f'{place} doese not exist')

def gettemp(place: str):
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    om = openmeteo_requests.Client()
    hourly = "temperature_2m"
    latitude, longitude = getlat(place)
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "current": hourly
    }
    response = om.weather_api(BASE_URL, params=params)
    output = response[0]
    hourly = output.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    temperature = hourly_temperature_2m
    return temperature, longitude, latitude

if __name__ == '__main__':

    place = input('give place:')

    # temperature, longitude, latitude = main(place)
    latitude, longitude = getlat(place)
    #print(f'current temperature in {place} is {temperature[0]}')
    print(f'Locations longatude and latitude is {longitude} and {latitude}')