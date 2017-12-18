"""
	Uses matplotlib and pandas to display various data about Iowa cities.
	Tim Coutinho
"""

import csv
import pygame as pg
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

df = pd.read_csv('iowa_cities.txt',index_col='name')

default_font = 'Calibri'
display_w = 800
display_h = 600

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
green = (0,255,0)
blue = (0,0,200)

pg.init()
game_display = pg.display.set_mode((display_w,display_h))
pg.display.set_caption('Iowa')
clock = pg.time.Clock()


def button(x,y,w,h,color1,color2=None,msg=None,msg_color=black,func=None):
	color = color1
	mouse = pg.mouse.get_pos()
	click = pg.mouse.get_pressed()
	font = pg.font.SysFont(default_font, 20)
	text, text_rect = make_text(msg, font, msg_color)
	text_rect.center = ((x + w/2, y + h/2))

	if mouse[0] in range(x, x+w) and mouse[1] in range(y, y+h):
		color = color2 if color2 else color1
		if click[0] == 1 and func:
			func()

	pg.draw.rect(game_display, color, (x,y,w,h))
	game_display.blit(text, text_rect)


def make_text(msg, font, color):
	surf = font.render(msg, True, color)
	return surf, surf.get_rect()


def draw_scatter():
	df.plot.scatter(x='longitude',y='latitude',s=df['population']/500,
					title='Iowa City Population')
	plt.show()


def draw_hex():
	df.plot.hexbin(x='longitude',y='latitude',gridsize=20,
				   title='Iowa City Density',cmap='coolwarm')
	plt.show()


def show_basemap():
	m = Basemap(projection='mill',llcrnrlat=40,llcrnrlon=-97,
									urcrnrlat=44,urcrnrlon=-90)
	m.drawstates(color='k')
	cities, pops, lats, lons = [], [], [], []

	with open('iowa_cities.txt', 'r') as f:
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

	plt.show()


def main_loop():
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
		game_display.fill(white)

		button(int(display_w*(1/5)),int(display_h/2),100,50,
			   green,blue,msg='Scatter',func=draw_scatter)
		button(int(display_w*(2/5)),int(display_h/2),100,50,
			   blue,green,msg = 'Hex',msg_color=white,func=draw_hex)
		button(int(display_w*(3/5)),int(display_h/2),100,50,
			   red,msg = 'Basemap',msg_color=white,func=show_basemap)

		pg.display.update()
		clock.tick(20)


main_loop()
pg.quit()
quit()
