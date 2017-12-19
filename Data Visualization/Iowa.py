"""
	Uses matplotlib and pandas to display various data about Iowa cities.
	Tim Coutinho
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

df = pd.read_csv('iowa_cities.csv',index_col='name')


def draw_scatter():
	df.plot.scatter(x='longitude',y='latitude',s=df['population']/500,
					title='Iowa City Population')


def draw_hex():
	df.plot.hexbin(x='longitude',y='latitude',gridsize=20,
				   title='Iowa City Density',cmap='coolwarm')


def draw_basemap():
	m = Basemap(projection='mill',llcrnrlat=40,llcrnrlon=-97,
								  urcrnrlat=44,urcrnrlon=-90)
	m.drawstates(color='k')
	cities, pops, lats, lons = [], [], [], []

	with open('iowa_cities.csv', 'r') as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			cities.append(row[1])
			lats.append(float(row[7]))
			lons.append(float(row[8]))
			pops.append(float(row[10]))

	for n, cities in enumerate(cities):
		if pops[n] > 50000:
			xpt, ypt = m(lons[n], lats[n])
			m.plot(xpt, ypt, 'co', markersize=5)


draw_hex()
draw_scatter()
draw_basemap()
plt.show()
