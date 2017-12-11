"""
	Utility written to help organize my music files.
	Lowercases all title/album words in no_upper,
	moves songs into folders if not in one already.
	Tim Coutinho
"""

import os
import re
from mutagen.easyid3 import EasyID3

no_upper = ('the', 'of', 'a', 'an', 'and', 'in', 'but','or',
			'for', 'nor', 'on', 'at', 'to', 'from', 'by')
good_ext = ('.aiff', '.ape', '.asf', '.flac', '.mp3', '.mp4', '.mpc',
			'.ofr', '.oga', '.ogg', '.ogv', '.opus', '.spx', '.tta', '.wv')
base = '/Users/tmcou/Music/iTunes/iTunes Media/Music'


def main():
	os.chdir(base)
	for artist in os.listdir():
		os.chdir(f'{base}/{artist}')
		print(artist)
		for album in os.listdir():
			if os.path.isfile(album):
				make_unknown(artist, album)		# Create Unknown Album folder
				modify_album(artist, f'{base}/{artist}/Unknown Album/{album}')
			else:
				modify_album(artist, album)


def make_unknown(artist, song):
	os.mkdir('Unknown Album')
	os.rename(f'{base}/{artist}/{song}',
			  f'{base}/{artist}/Unknown Album/{song}')


def modify_album(artist, album):
	os.chdir(f'{base}/{artist}/{album}')
	for song in os.listdir():
		if os.path.splitext(song)[1] in good_ext:	# Valid audio extension
			modify_song(song)


def modify_song(song):
	audio = EasyID3(song)
	# Removes any leading album identifiers, i.e. 01 and 13 -
	song_name = re.sub(r'^\d+\-?\d+\.? ?\-? ', '',
					   os.path.splitext(song)[0]).lower()
	try:	# In an album, tag exists
		audio['album'] = ' '.join([word if word in no_upper
								        else word.capitalize()
								        for word
								        in audio['album'][0].lower().split()])
	except Exception:	# Not in an album, tag does't exist
		pass
	audio['title'] = ' '.join([word if word.lower() in no_upper
							        else word.capitalize()
							        for word in song_name.split()])
	# Capitalize the first word regardless
	audio['title'] = audio['title'][0][0].upper() + audio['title'][0][1:]
	audio.save()


if __name__ == '__main__':
	main()
