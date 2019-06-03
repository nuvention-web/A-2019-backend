import requests
import pytemperature


def getWeatherInfo():
    api_address = 'http://api.openweathermap.org/data/2.5/weather?q=Evanston,us&APPID=00635a2705abb24f3c1e116788d7614e'
    json_data = requests.get(url=api_address).json()
    formatted_data = json_data['main']
    temperature = pytemperature.k2c(formatted_data['temp'])
    return round(temperature, 2)