"""
	An API Key test using Wunderground's API to
	fetch weather data on the city of choice.
	Tim Coutinho
"""

import time
import json
from urllib.request import urlopen
from constants import key, us_state_abbrev

def main():
	yes = ('yes', 'ye', 'y')
	no = ('no', 'n')
	bys = {'city':byCity, 'cities':byCity, 'zip':byZip, 'zips':byZip, 'coord':byCoords,'coords':byCoords, 'coordinates':byCoords}
	city, state, zip, temp, wind, gust = bys[input("By city, zip, or coords? ").lower()]()	# Uses input to call corresponding function with bys dict

	print("The weather in {}, {} is currently {}.".format(city, state, temp))
	print("{} is currently experiencing {} mph winds with gusts up to {} miles per hour.".format(city, wind, gust))
	if input("Continue?\n").lower() in yes:
		main()
	print('Farewell!')
	time.sleep(1)

def byCity(city=None, state=None):
	if city == state == None:	# Function called naturally by user
		state = input("Enter state: ")
		state = us_state_abbrev.get(state.lower().capitalize(), state)
		city = input("Enter city: ").replace(" ", "_")
	with urlopen('http://api.wunderground.com/api/{}/conditions/q/{}/{}.json'.format(key, state, city)) as url:
		data = json.loads(url.read().decode())	# .load() is for files, .loads() is for strings, url.read() returns a string
	return (data["current_observation"]["display_location"]["city"],
		    data["current_observation"]["display_location"]["state"],
		    data["current_observation"]["display_location"]["zip"],
		    data["current_observation"]["temperature_string"],
		    data["current_observation"]["wind_mph"],
		    data["current_observation"]["wind_gust_mph"])

def byZip():
	zip = input("Enter zip code: ")
	with urlopen('http://api.wunderground.com/api/{}/geolookup/q/{}.json'.format(key, zip)) as url:
		data = json.loads(url.read().decode())
	return byCity(data["location"]["city"], data["location"]["state"])	# Needed to pull weather condition data, not in zip json

def byCoords():
	lat, lon = input("Enter latitude, longitude: ").replace(' ', '').split(',')
	with urlopen('http://api.wunderground.com/api/{}/geolookup/q/{},{}.json'.format(key, lat, lon)) as url:
		data = json.loads(url.read().decode())
	return byCity(data["location"]["city"], data["location"]["state"])	# Needed to pull weather condition data, not in coords json

if __name__ == '__main__':
	main()