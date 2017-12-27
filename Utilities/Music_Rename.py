"""
	Utility written to help organize my music files.
	Lowercases all title/album words in NO_UPPER,
	moves songs into folders if not in one already.
	USE MUSIC - COPY FIRST
	Tim Coutinho
"""

import os
import re
from contextlib import contextmanager

from mutagen.easyid3 import EasyID3

NO_UPPER = ('a', 'an', 'and', 'at', 'but', 'by', 'for','from',
			'in', 'nor', 'of', 'on', 'or', 'the', 'to')
GOOD_EXT = ('.aiff', '.ape', '.asf', '.flac', '.mp3', '.mp4', '.mpc',
			'.ofr', '.oga', '.ogg', '.ogv', '.opus', '.spx', '.tta', '.wv')
ROMAN_NUMS = ('Ii', 'Iii', 'Iv', 'Vi', 'Vii', 'Viii', 'Ix')
BASE = '/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy'

pathify = lambda *paths: '\\'.join(paths)


@contextmanager
def open_audio(song):
	"""Automatically save audio file once done editing."""
	try:
		audio = EasyID3(''.join(song))
		yield audio
	finally:
		audio.save()


def make_unknown(artist, song):
	"""Move a song from the artist folder to an Unknown Album folder."""
	os.mkdir('Unknown Album')
	os.rename(pathify(BASE,artist,song),
			  pathify(BASE,artist,'Unknown Album',song))
	return 'Unknown Album'


def modify_album(artist, album):
	"""Modifies all valid audio files in an album"""
	if album != 'Unknown Album':
		print(f'  {album}')
	os.chdir(pathify(BASE,artist,album))
	for song in os.listdir():
		song = os.path.splitext(song)
		try:
			with open_audio(song) as audio:
				if audio:
					modify_song(song, audio)
		except Exception:  # Invalid audio extension
			pass
		# if song[1] not in GOOD_EXT:  # Valid audio extension
		# 	continue
		# with open_audio(song) as audio:
		# 	modify_song(song, audio)


def modify_song(song, audio):
	"""Modify a song's title and album tags."""
	try:
		modify_tag(song, audio, 'album')
	except Exception:  # Not in an album, tag does't exist
		pass
	if 'title' not in audio:  # Use file name as title
		sub = r'[^\w\d,])[ \-\.]*'
		if 'album' in audio:
			sub = r'^([0-2]?[\d]' + sub
		# Removes any leading album identifiers, i.e. '01' and '13 -'
		audio['title'] = re.sub(r'^([0-2]?[\d][^\w\d,])[ \-\.]*',
								'', song[0].lstrip('0'))
	modify_tag(song, audio, 'title')


def modify_tag(orig, audio, tag):
	"""Change a specific tag of a song."""
	# Makes directory navigation easier, adding spaces around any /
	audio[tag] = audio[tag][0].replace('/', ' / ')
	audio[tag] = ' '.join([word if re.sub(r'[:/\-]', '', word)
						   in NO_UPPER else word.capitalize()
						   for word in audio[tag][0].split()])
	# Edge Cases:
	# Roman numerals
	if any(word.strip(':') in ROMAN_NUMS for word in audio[tag][0].split()):
		for word in audio[tag][0].split():
			if word.strip(':') in ROMAN_NUMS:
				audio[tag] = audio[tag][0].replace(word, word.upper())
	# Underscores (title likely pulled from file name)
	while '_' in audio[tag][0]:
		c = input(f'What character should replace the _ in {audio[tag][0]}? ')
		audio[tag] = audio[tag][0].replace('_', c, 1)
	# Parentheses, colons, ellipses
	matches = re.findall(r'[\(:\.]+ *[a-z]', audio[tag][0])
	for match in matches:
		audio[tag] = audio[tag][0].replace(match, match.upper())
	# Finally, capitalize the first word regardless
	audio[tag] = audio[tag][0][0].upper() + audio[tag][0][1:]

	# sub = re.sub(r'[/:\?]', '_', audio[tag][0])
	# if tag == 'title' and 'album' in audio:  # Rename file to new song title
	# 	os.rename(pathify(BASE,audio['artist'][0],
	# 					  audio['album'][0].replace('/', '_'),''.join(orig)),
	# 			  pathify(BASE,audio['artist'][0],
	# 			  		  audio['album'][0].replace('/', '_'),sub)+orig[1])
	# 	os.remove(pathify(BASE,audio['artist'][0],
	# 					  audio['album'][0].replace('/', '_'),''.join(orig)))
	# elif tag == 'title':
	# 	os.rename(pathify(BASE,audio['artist'][0],
	# 					  'Unknown Album',''.join(orig)),
	# 			  pathify(BASE,audio['artist'][0],
	# 			  		  'Unknown Album',sub)+orig[1])
	# 	os.remove(pathify(BASE,audio['artist'][0],
	# 					  'Unknown Album',''.join(orig)))


def individual(directory):
	"""Separate utility to modify any audio files in one directory."""
	os.chdir(directory)
	for song in os.listdir():
		song = os.path.splitext(song)
		if song[1] in GOOD_EXT:  # Valid audio extension
			print(song[0])
			with open_audio(song) as audio:
				if 'title' in audio:
					del audio['title']
				modify_song(song, audio)

def main():
	os.chdir(BASE)
	for artist in os.listdir():
		os.chdir(pathify(BASE, artist))
		print(artist)
		for album in os.listdir():
			if os.path.isfile(album):  # Create Unknown Album folder
				album = make_unknown(artist, album)
			modify_album(artist, album)


if __name__ == '__main__':
	main()
	# individual('/Users/tmcou/Downloads')
