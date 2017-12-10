"""
	Utility written to help organize my music files.
	
	Tim Coutinho
"""

import os
import re
from mutagen.easyid3 import EasyID3

no_upper = ('the', 'of', 'a', 'an', 'and', 'in', 'but','or',
			'for', 'nor', 'on', 'at', 'to', 'from', 'by')
good_ext = ('.mp3', '.mp4', '.flac', '.aiff', '.ape', '.tta', '.wv', '.mpc',
			'.opus', '.spx', '.flac', '.ogg', '.oga', '.ogv', '.asf', '.ofr')
base = '/Users/tmcou/Music/iTunes/iTunes Media/Music'


def main():
	os.chdir(base)
	for artist in os.listdir():
		os.chdir(f'{base}/{artist}')
		print(artist)
		for album in os.listdir():
			if os.path.isfile(album):
				os.mkdir('Unknown Album')
				os.rename(f'{base}/{artist}/{album}',
						  f'{base}/{artist}/Unknown Album/{album}')
			else:
				modify_album(artist, album)


def modify_album(artist, album):
	os.chdir(f'{base}/{artist}/{album}')
	for song in os.listdir():
		if os.path.splitext(song)[1] in good_ext:
			modify_song(song)
		# try:
		# 	modify_song(song)
		# except Exception:
		# 	continue


def modify_song(song):
	audio = EasyID3(song)
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
