from urllib.request import urlopen
from requests import get
import json
import urllib
import sys


def get_ip_addr():
    # This function returns the local computer IP address
    ip = get('https://api.ipify.org').text
    return ip


def get_geo_location():
    # This function returns the geographic location of an IP address
    ip = get_ip_addr()
    url = "http://ip-api.com/json/{0}".format(ip)
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    return city


def build_url(city):
    # This function gets a city name, and builds the correct URL to access the API of OpenWeatherMap site
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q='
    user_apikey = "0f70a5c0190eca8ca6ad878d1c39d272"
    units = 'metric'
    url = api_url + city + '&mode=json&units=' + units + '&APPID=' + user_apikey
    #print(url)
    return url


def get_weather(city):
    # This function opens the URL, and gets the temperature and country code into a tupel
    url = urllib.request.urlopen(build_url(city))
    output = url.read().decode('utf-8')
    data = json.loads(output)
    url.close()
    return (
        data.get('main').get('temp'), data.get('sys').get('country'))  # tupel to return 2 values: city and country code


def print_to_text():
    # This function writes into a regular text file the temperature of the city that the
    # local computer who runs the python script is located at
    city = get_geo_location()
    text_file = open("Output.txt", "w")
    text_file.write(str(get_weather(city)[0]))
    text_file.close()


def country_code_to_country(country_code):
    # This function gets a country code (OpenWeatherMap provide full country code in their API)
    # and translates the country code to a full country name
    url = "http://restcountries.eu/rest/v2/alpha/{0}".format(country_code)
    response = urlopen(url)
    data = json.load(response)
    country = data['name']
    return country


def cities_weather():
    # This function prints the current temperature of 10 worldwide cities
    cities = ['Paris', 'Haifa', 'New York', 'Berlin', 'Moscow', 'Amsterdam', 'Hamburg', 'Vienna', 'Tokyo',
              'Melbourne']
    for city in cities:
        temp, country_code = get_weather(city)  # Split the returned tupel to 2 strings, temperature and country code
        country = country_code_to_country(country_code)  # Translate country code to full country name
        print("The weather in " + city + ", " + country + " is " + str(temp) + " degrees")


def main():
    # This is the main function who starts 2 functions
    #print_to_text()
    #cities_weather()
    print("Enter a city name:")
    city = sys.argv[0:]
    print(get_weather(city))



if __name__ == "__main__":
    main()
