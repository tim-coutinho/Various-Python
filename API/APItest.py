'''
	An API test using Wunderground's API to fetch
	weather data on the city/zip/coordinates of choice.
	Tim Coutinho
'''

import time
import json
from datetime import datetime
from urllib.request import urlopen
from constants import key, us_state_abbrev

yes = ('yes', 'ye', 'y')
no = ('no', 'n')


def printData():
	bys = {'city':byCity, 'cities':byCity, 'zip':byZip, 'zips':byZip,
		   'coord':byCoords,'coords':byCoords, 'coordinates':byCoords}
	# Uses bys dict to call corresponding function based on input
	(city, state, zip,
	temp, wind, gust, time) = bys[input('By city, zip, or coords? ').lower()]()
	print(f'As of {time}, the weather in {city}, {state} is {temp}.')
	print(f'{city} is currently experiencing {wind} mph '
		  f'winds with gusts up to {gust} miles per hour.')


def byCity(city=None, state=None):
	if city == state == None:	# Function called naturally by user
		state = input('Enter state: ')
		state = us_state_abbrev.get(state.lower().capitalize(), state)
		city = input('Enter city: ').replace(' ', '_')
	with urlopen(f'http://api.wunderground.com/api/{key}/conditions/q/{state}/{city}.json') as url:
		data = json.loads(url.read().decode())
	return (data['current_observation']['display_location']['city'],
		    data['current_observation']['display_location']['state'],
		    data['current_observation']['display_location']['zip'],
		    data['current_observation']['temperature_string'],
		    data['current_observation']['wind_mph'],
		    data['current_observation']['wind_gust_mph'],
		    data['current_observation']['observation_time'].split(', ')[1])


def byZip():
	zip = input('Enter zip code: ')
	with urlopen(f'http://api.wunderground.com/api/{key}/geolookup/q/{zip}.json') as url:
		data = json.loads(url.read().decode())
	# Needed to pull weather condition data, doesn't exist in zip json
	return byCity(data['location']['city'], data['location']['state'])


def byCoords():
	lat, lon = input('Enter latitude, longitude: ').replace(' ', '').split(',')
	with urlopen(f'http://api.wunderground.com/api/{key}/geolookup/q/{lat},{lon}.json') as url:
		data = json.loads(url.read().decode())
	return byCity(data['location']['city'], data['location']['state'])


def main():
	try:
		printData()
	except Exception as e:
	 	print('Invalid input.')

	if input('Continue? ').lower() in yes:
		main()
	print('\nFarewell!')
	time.sleep(1)


if __name__ == '__main__':
	main()
