"""
	Uses matplotlib and pandas to display various data about Iowa cities.
	Tim Coutinho
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('iowa_cities.txt',index_col='name')
#print(df.head())
# m = Basemap(projection='mill', llcrnrlat=40, llcrnrlon=-97, urcrnrlat=44, urcrnrlon=-90)
# m.drawcoastlines()
# m.drawcountries()
# m.drawstates(color='k')

cities, pops, lats, lons = [], [], [], []

readfile = open('iowa_cities.txt', 'r')

for row in readfile:
	if 'zip_code' not in row:
		row = row.split(',')
		cities.append(row[1])
		lats.append(float(row[7]))
		lons.append(float(row[8]))
		pops.append(float(row[10]))



for n, cities in enumerate(cities):
	pass
	#if pops[n] > 50000:
	#xpt, ypt = m(lons[n], lats[n])
	#m.plot(xpt, ypt, 'co', markersize=5)

df.plot.scatter(x='longitude',y='latitude',s=df['population']/500)
#df.plot.hexbin(x='longitude',y='latitude',gridsize=15,cmap='coolwarm')
plt.show()