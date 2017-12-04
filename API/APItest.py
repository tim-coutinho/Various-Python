"""
	An API Key test using Wunderground's API to
	fetch weather data on the city of choice.
	Tim Coutinho
"""

import json
import urllib.request
from key import key

# with open('temp.json', 'r+') as temp:
# 	data = json.load(temp)
# 	temp.seek(0)
# 	data["b"] = 4
# 	json.dump(data, temp)
# print(data)

state = input("Enter two letter state abbreviation: ")
city = input("Enter city: ").replace(" ", "_")
with urllib.request.urlopen('http://api.wunderground.com/api/{}/conditions/q/{}/{}.json'.format(key, state, city)) as url:
	data = json.loads(url.read().decode())
state = data["current_observation"]["display_location"]["state"]
city = data["current_observation"]["display_location"]["city"]

print("The weather in {}, {} is currently {}.".format(city, state, data["current_observation"]["temperature_string"]))
print("{} is currently experiencing {} winds with gusts up to {} miles per hour.".format(city, data["current_observation"]["wind_string"].lower(),
																						 data["current_observation"]["wind_gust_mph"]))