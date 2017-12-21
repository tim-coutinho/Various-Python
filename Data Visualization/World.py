'''
	Uses matplotlib and pandas to display various data about the world.
	CSV file currently missing.
	Tim Coutinho
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('worldcitiespop.csv')
df = df[(df['Country'] == 'us') & ((df['Latitude'] < 50) & (df['Latitude'] > 23)) & ((df['Longitude']<-67) & (df['Longitude']>-130))]
df.drop(['AccentCity'], axis=1, inplace=True)
#df.plot.scatter(x='Longitude',y='Latitude',s=0.5)
print(df.info())
#print(df['Region'].head())
#df.plot.bar(x='Region',y='Population')
#df.plot.hexbin(x='Longitude',y='Latitude',gridsize=25)
plt.show()