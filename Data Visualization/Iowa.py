"""
	Uses matplotlib and pandas to display various data about Iowa cities.
	Tim Coutinho
"""

import csv
import pygame as pg
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

pg.init()
display_w = 800
display_h = 600
default_font = 'Calibri'

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
green = (0,255,0)
blue = (0,0,200)

game_display = pg.display.set_mode((display_w,display_h))
pg.display.set_caption('Iowa')
clock = pg.time.Clock()


def button(x,y,w,h,color1,color2=None,msg=None,msg_color=black,func=None):
	if not color2:
		color2 = color1
	mouse = pg.mouse.get_pos()
	click = pg.mouse.get_pressed()

	if mouse[0] in range(x, x+w) and mouse[1] in range(y, y+h):
		pg.draw.rect(game_display, color2, (x,y,w,h))
		if click[0] == 1 and func:
			func()
	else:
		pg.draw.rect(game_display, color1, (x,y,w,h))
	font = pg.font.SysFont(default_font, 20)
	text, text_rect = make_text(msg, font, msg_color)
	text_rect.center = ((x + w/2, y + h/2))
	game_display.blit(text, text_rect)


def make_text(msg, font, color):
	surf = font.render(msg, True, color)
	return surf, surf.get_rect()


def show_scatter():
	df.plot.scatter(x='longitude',y='latitude',s=df['population']/500)
	plt.show()


def show_hex():
	df.plot.hexbin(x='longitude',y='latitude',gridsize=15,cmap='coolwarm')
	plt.show()


def main_loop():
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
		game_display.fill(white)
		button(int(display_w/3),int(display_h/2),100,50,
			   green,blue,msg='Scatter',func=show_scatter)
		button(int(display_w/2),int(display_h/2),100,50,
			   blue,green,msg = 'Hex',msg_color=white,func=show_hex)
		pg.display.update()
		clock.tick(20)


# m = Basemap(projection='mill',llcrnrlat=40,llcrnrlon=-97,
#								urcrnrlat=44,urcrnrlon=-90)
# m.drawcoastlines()
# m.drawcountries()
# m.drawstates(color='k')
# cities, pops, lats, lons = [], [], [], []
# with open('iowa_cities.txt', 'r') as f:
# 	reader = csv.reader(f)
# 	next(reader)
# 	for row in reader:
# 		cities.append(row[1])
# 		lats.append(float(row[7]))
# 		lons.append(float(row[8]))
# 		pops.append(float(row[10]))

# for n, cities in enumerate(cities):
# 	if pops[n] > 50000:
# 		xpt, ypt = m(lons[n], lats[n])
# 		m.plot(xpt, ypt, 'co', markersize=5)

df = pd.read_csv('iowa_cities.txt',index_col='name')
main_loop()
# df.plot.scatter(x='longitude',y='latitude',s=df['population']/500)
# df.plot.hexbin(x='longitude',y='latitude',gridsize=15,cmap='coolwarm')
# plt.show()
pg.quit()
quit()