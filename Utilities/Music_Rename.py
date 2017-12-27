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
from mutagen.id3._util import ID3NoHeaderError

NO_UPPER = ('a', 'an', 'and', 'at', 'but', 'by', 'for','from',
			'in', 'nor', 'of', 'on', 'or', 'the', 'to')
GOOD_EXT = ('.aiff', '.ape', '.asf', '.flac', '.mp3', '.mp4', '.mpc',
			'.ofr', '.oga', '.ogg', '.ogv', '.opus', '.spx', '.tta', '.wv')
ROMAN_NUMS = ('Ii', 'Iii', 'Iv', 'Vi', 'Vii', 'Viii', 'Ix')
modified = 0

pathify = lambda *paths: '/'.join(paths)

re_nums = re.compile(r'^[0-1]?[\d]\W[.\- ]*')
re_parens = re.compile(r'[\(:\.]+ *[a-z]')
re_spec = re.compile(r'[:/\-]')


@contextmanager
def open_audio(song):
	"""Automatically save audio file once done editing."""
	try:
		audio = EasyID3(''.join(song))
		yield audio
	except ID3NoHeaderError:
		yield
	else:
		audio.save()


def make_unknown(base, artist, song):
	"""Move a song from the artist folder to an Unknown Album folder."""
	os.chdir(pathify(base,artist))
	os.mkdir('Unknown Album')
	os.rename(pathify(base,artist,song),
			  pathify(base,artist,'Unknown Album',song))
	os.chdir(pathify(base,artist,album))
	return 'Unknown Album'


def modify_album(base, artist, album, individual=False):
	"""Modifies all valid audio files in an album."""
	if album != 'Unknown Album':
		print(f'  {album}')
	try:
		os.chdir(pathify(base,artist,album))
	except NotADirectoryError:
		album = make_unknown(base,artist,album)
	for song in os.listdir():
		song = os.path.splitext(song)
		with open_audio(song) as audio:
			if audio:
				if individual:
					print(song[0])
					if 'title' in audio:
						del audio['title']
				modify_song(base, song, audio)


def modify_song(base, song, audio):
	"""Modify a song's title and album tags."""
	global modified
	try:
		modify_tag(base, song, audio, 'album')
	except KeyError:  # Not in an album, tag does't exist
		pass
	if 'title' not in audio:  # Use file name as title
		# Removes any leading album identifiers, i.e. '01' and '13 -'
		audio['title'] = re_nums.sub('', song[0].lstrip('0'))
	modify_tag(base, song, audio, 'title')
	modified += 1


def modify_tag(base, orig, audio, tag):
	"""Change a specific tag of a song."""
	# Makes directory navigation easier, adding spaces around any /
	audio[tag] = audio[tag][0].replace('/', ' / ')
	audio[tag] = ' '.join([word if re_spec.sub('', word)
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
	matches = re_parens.findall(audio[tag][0])
	for match in matches:
		audio[tag] = audio[tag][0].replace(match, match.upper())
	# Finally, capitalize the first word regardless
	audio[tag] = audio[tag][0][0].upper() + audio[tag][0][1:]

	# sub = re.sub(r'[/:\?]', '_', audio[tag][0])
	# if tag == 'title' and 'album' in audio:  # Rename file to new song title
	# 	os.rename(pathify(base,audio['artist'][0],
	# 					  audio['album'][0].replace('/', '_'),''.join(orig)),
	# 			  pathify(base,audio['artist'][0],
	# 			  		  audio['album'][0].replace('/', '_'),sub)+orig[1])
	# 	os.remove(pathify(base,audio['artist'][0],
	# 					  audio['album'][0].replace('/', '_'),''.join(orig)))
	# elif tag == 'title':
	# 	os.rename(pathify(base,audio['artist'][0],
	# 					  'Unknown Album',''.join(orig)),
	# 			  pathify(base,audio['artist'][0],
	# 			  		  'Unknown Album',sub)+orig[1])
	# 	os.remove(pathify(base,audio['artist'][0],
	# 					  'Unknown Album',''.join(orig)))


def main():
	base = '/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy'
	os.chdir(base)
	for artist in os.listdir():
		print(artist)
		os.chdir(pathify(base, artist))
		for album in os.listdir():
			modify_album(base, artist, album)


if __name__ == '__main__':
	main()
	# modify_album('/Users', 'tmcou', 'Downloads')
	print(f'\nModified {modified} songs.')
