"""
	Uses matplotlib and pandas to display various data about Iowa cities.
	Tim Coutinho
"""

from mpl_toolkits.basemap import Basemap
import csv
import matplotlib.pyplot as plt
import pandas as pd

# m = Basemap(projection='mill', llcrnrlat=40, llcrnrlon=-97, urcrnrlat=44, urcrnrlon=-90)
# m.drawcoastlines()
# m.drawcountries()
# m.drawstates(color='k')
# cities, pops, lats, lons = [], [], [], []
# with open('iowa_cities.txt', 'r') as f:
# 	reader = csv.reader(f)
# 	next(reader)
# 	for row in reader:
# 		if 'zip_code' not in row:
# 			cities.append(row[1])
# 			lats.append(float(row[7]))
# 			lons.append(float(row[8]))
# 			pops.append(float(row[10]))

# for n, cities in enumerate(cities):
# 	if pops[n] > 50000:
# 		xpt, ypt = m(lons[n], lats[n])
# 		m.plot(xpt, ypt, 'co', markersize=5)

df = pd.read_csv('iowa_cities.txt',index_col='name')
df.plot.scatter(x='longitude',y='latitude',s=df['population']/500)
# df.plot.hexbin(x='longitude',y='latitude',gridsize=15,cmap='coolwarm')
plt.show()