"""
	An API Key test using Wunderground's API to
	fetch weather data on the city of choice.
	Tim Coutinho
"""

import time
import json
from urllib.request import urlopen
from constants import key, us_state_abbrev

yes = ('yes', 'ye', 'y')
no = ('no', 'n')

def main():
	try:
		printData()
	except Exception as e:
		print('Invalid input.')

	if input("Continue? ").lower() in yes:
		main()
	print('\nFarewell!')
	time.sleep(1)

def printData():
	bys = {'city':byCity, 'cities':byCity, 'zip':byZip, 'zips':byZip, 'coord':byCoords,'coords':byCoords, 'coordinates':byCoords}
	city, state, zip, temp, wind, gust = bys[input("By city, zip, or coords? ").lower()]()	# Uses input to call corresponding function
	print(f"The weather in {city}, {state} is currently {temp}.")							# with bys dict
	print(f"{city} is currently experiencing {wind} mph winds with gusts up to {gust} miles per hour.")
	# if input("Show nearby cities' data? ").lower() in yes:
	# 	showNearby(city, state)

def byCity(city=None, state=None):
	if city == state == None:	# Function called naturally by user
		state = input("Enter state: ")
		state = us_state_abbrev.get(state.lower().capitalize(), state)
		city = input("Enter city: ").replace(" ", "_")
	with urlopen(f'http://api.wunderground.com/api/{key}/conditions/q/{state}/{city}.json') as url:
		data = json.loads(url.read().decode())	# .load() is for files, .loads() is for strings, url.read() returns a string
	return (data["current_observation"]["display_location"]["city"],
		    data["current_observation"]["display_location"]["state"],
		    data["current_observation"]["display_location"]["zip"],
		    data["current_observation"]["temperature_string"],
		    data["current_observation"]["wind_mph"],
		    data["current_observation"]["wind_gust_mph"])

def byZip():
	zip = input("Enter zip code: ")
	with urlopen(f'http://api.wunderground.com/api/{key}/geolookup/q/{zip}.json') as url:
		data = json.loads(url.read().decode())
	return byCity(data["location"]["city"], data["location"]["state"])	# Needed to pull weather condition data, doesn't exist in zip json

def byCoords():
	lat, lon = input("Enter latitude, longitude: ").replace(' ', '').split(',')
	with urlopen(f'http://api.wunderground.com/api/{key}/geolookup/q/{lat},{lon}.json') as url:
		data = json.loads(url.read().decode())
	return byCity(data["location"]["city"], data["location"]["state"])	# Needed to pull weather condition data, doesn't exist in coords json

# def showNearby(city, state):
# 	with urlopen(f'http://api.wunderground.com/api/{key}/geolookup/q/{state}/{city}.json') as url:
# 		data = json.loads(url.read().decode())
# 	for station in data["location"]["nearby_weather_stations"]["airport"]["station"]:
# 		byCity(station["city"], station["state"])

if __name__ == '__main__':
	main()