"""
	Expands on the data visualization aspect
	of iowa.py, adds a GUI, buttons, etc.
	Tim Coutinho
"""

import csv
from contextlib import contextmanager

import pygame as pg
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

df = pd.read_csv('iowa_cities.csv',index_col='name')

DEFAULT_FONT = 'Calibri'
DISPLAY_W = 800
DISPLAY_H = 600

COLORS = {'white': (255,255,255),'black':   (0,0,0),  'red':    (255,0,0),
		  'green': (0,255,0),    'blue':    (0,0,200),'yellow': (255,255,0),
		  'cyan':  (0,255,255),  'magenta': (255,0,255)}

game_display = pg.display.set_mode((DISPLAY_W,DISPLAY_H))
pg.display.set_caption('Iowa')
clock = pg.time.Clock()


@contextmanager
def begin():
	try:
		pg.init()
		yield
	finally:
		pg.quit()
		quit()


def button(x,y,w,h,color1,color2=None,msg=None,
		   msg_color=COLORS['black'],func=None):
	color = color1
	mouse = pg.mouse.get_pos()
	lclick = pg.mouse.get_pressed()[0]
	font = pg.font.SysFont(DEFAULT_FONT, 20)
	text, text_rect = make_text(msg, font, msg_color)
	text_rect.center = ((x + w/2, y + h/2))

	if mouse[0] in range(x, x+w) and mouse[1] in range(y, y+h):
		color = color2 or color1  # Sets to color1 if color2 is None
		if lclick == 1 and func:
			[f() for f in func]

	pg.draw.rect(game_display, color, (x,y,w,h))
	game_display.blit(text, text_rect)


def make_text(msg, font, color):
	surf = font.render(msg, True, color)
	return surf, surf.get_rect()


def draw_scatter():
	df.plot.scatter(x='longitude',y='latitude',s=df['population']/500,
					title='Iowa City Population')


def draw_hex():
	df.plot.hexbin(x='longitude',y='latitude',gridsize=20,
				   title='Iowa City Density',cmap='coolwarm')


def draw_basemap():
	m = Basemap(projection='mill',llcrnrlat=40,llcrnrlon=-97,
				urcrnrlat=44,urcrnrlon=-90,resolution='l')
	m.drawstates(color='k')
	m.drawrivers()
	cities, pops, lats, lons = [], [], [], []

	with open('iowa_cities.csv') as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			cities.append(row[1])
			lats.append(float(row[7]))
			lons.append(float(row[8]))
			pops.append(float(row[10]))

	for pop, lat, lon in zip(pops, lats, lons):
		if pop > 50000:
			x, y = m(lon, lat)
			m.plot(x, y, 'co', markersize=5)


def main_loop():
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
		game_display.fill(COLORS['white'])

		button(int(DISPLAY_W*.25 - 50),int(DISPLAY_H*.4),100,50,
			   COLORS['green'],COLORS['blue'],msg='Scatter',
			   func=(draw_scatter,plt.show))
		button(int(DISPLAY_W*.5 - 50),int(DISPLAY_H*.4),100,50,COLORS['blue'],
			   COLORS['green'],msg='Hex',msg_color=COLORS['white'],
			   func=(draw_hex,plt.show))
		button(int(DISPLAY_W*.75 - 50),int(DISPLAY_H*.4),100,50,
			   COLORS['magenta'],COLORS['cyan'],msg='Basemap',
			   func=(draw_basemap,plt.show))
		button(int(DISPLAY_W*.5 - 50),int(DISPLAY_H*.6),100,50,
			   COLORS['cyan'],COLORS['yellow'],msg='All',
			   func=(draw_scatter,draw_hex,draw_basemap,plt.show))
		button(int(DISPLAY_W*.5 - 50),int(DISPLAY_H*.9),100,50,COLORS['black'],
			   COLORS['red'],msg='Quit',msg_color=COLORS['white'],
			   func=(pg.quit,quit))

		pg.display.update()
		clock.tick(20)


def main():
	# I just really like context managers
	with begin():
		main_loop()
	# pg.init()
	# main_loop()
	# pg.quit()
	# quit()


if __name__ == '__main__':
	main()
