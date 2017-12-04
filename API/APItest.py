"""
	An API Key test using Wunderground's API to
	fetch weather data on the city of choice.
	Tim Coutinho
"""

import json
import urllib.request
from key import key

def main():
	data = byCity()
	zipData = byZip()
	coordData = byCoords()
	zip = data["current_observation"]["display_location"]["zip"]
	state = data["current_observation"]["display_location"]["state"]
	city = data["current_observation"]["display_location"]["city"]

	print("The weather in {}, {} is currently {}.".format(city, state, data["current_observation"]["temperature_string"]))
	print("{} is currently experiencing {} winds with gusts up to {} miles per hour.".format(city, data["current_observation"]["wind_string"].lower(),
																							 data["current_observation"]["wind_gust_mph"]))

def byCity():
	state = input("Enter two letter state abbreviation: ")
	city = input("Enter city: ").replace(" ", "_")
	with urllib.request.urlopen('http://api.wunderground.com/api/{}/conditions/q/{}/{}.json'.format(key, state, city)) as url:
		return json.loads(url.read().decode())

def byZip():
	zip = input("Enter zip code: ")
	with urllib.request.urlopen('http://api.wunderground.com/api/{}/geolookup/q/{}.json'.format(key, zip)) as url:
		return json.loads(url.read().decode())

def byCoords():
	lat, lon = input("Enter latitude, longitude: ").replace(' ', '').split(',')
	with urllib.request.urlopen('http://api.wunderground.com/api/{}/geolookup/q/{},{}.json'.format(key, lat, lon)) as url:
		return json.loads(url.read().decode())

if __name__ == '__main__':
	main()