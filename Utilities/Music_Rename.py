"""
	Utility written to help organize my music files.
	Lowercases all title/album words in NO_UPPER,
	moves songs into folders if not in one already.
	Accepts: .aiff, .ape, .asf, .flac, .mp3, .mp4, .mpc,
	.ofr, .oga, .ogg, .ogv, .opus, .spx, .tta, and .wv
	USE MUSIC - COPY FIRST, run tests beforehand.
	Tim Coutinho
"""

import os
import re
from pathlib import Path
from contextlib import contextmanager

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

NO_UPPER = ('a', 'an', 'and', 'at', 'but', 'by', 'de', 'for',
			'from', 'in', 'nor', 'of', 'on', 'or', 'the', 'to')
EXCEPTIONS = {'adhd': 'ADHD', 'id': 'ID', 'sea is a lady': 'SEA IS A LADY',
			  'i want! i want!': 'i want! i want!',
			  'futuresex  /  lovesounds': 'FutureSex / LoveSounds'}
ROMAN_NUMS = ('Ii', 'Iii', 'Iv', 'Vi', 'Vii', 'Viii', 'Ix')

re_nums = re.compile(r'^[0-1]?[\d]\W[.\- ]*')
re_parens = re.compile(r'[\(:\.]+ *[a-z]')
re_spec = re.compile(r'[:/\-]')


@contextmanager
def open_audio(song):
	"""Automatically save audio file once done editing."""
	try:
		audio = EasyID3(song)
		yield audio
	except ID3NoHeaderError:
		yield
	else:
		audio.save()


def make_unknown(song_path):
	"""Move a song from the artist folder to an Unknown Album folder."""
	(song_path.parent/'Unknown Album').mkdir()
	song_path.rename(song_path.parent/'Unknown Album'/song_path.name)
	return 'Unknown Album'


def modify_album(album_path, individual=False):
	"""Modifies all valid audio files in an album. Individual being true
	   indicates Music_Rename is being run on a single album or folder,
	   and not a whole music library."""
	modified = 0
	for song in os.scandir(album_path):
		if os.path.isdir(song.name):
			continue
		with open_audio(os.path.join(album_path, song.name)) as audio:
			if audio:
				old = dict(audio)
				if individual:
					print(os.path.splitext(song.name)[0])
					if 'title' in audio:
						del audio['title']
				modify_song(song.name, audio)
				modified += 1 if old != audio else 0
	return modified


def modify_song(song, audio):
	"""Modify a song's title and album tags."""
	try:
		audio['album'] = [modify_tag(audio['album'][0])]
	except KeyError:  # Not in an album, tag doesn't exist
		pass
	if 'title' not in audio:  # Use file name as title
		# Removes any leading album identifiers, i.e. '01' and '13 -'
		audio['title'] = re_nums.sub('', os.path.splitext(song)[0])
	audio['title'] = [modify_tag(audio['title'][0])]


def modify_tag(tag):
	"""Change a specific tag of a song."""
	# Makes directory navigation easier, adding spaces around any /
	tag = tag.replace('/', ' / ')
	if tag.lower() in EXCEPTIONS:
		return EXCEPTIONS[tag.lower()]
	tag = ' '.join([word if re_spec.sub('', word) in NO_UPPER
					else word.capitalize() for word in tag.split()])
	tag = edge_cases(tag)
	# Finally, capitalize the first word regardless
	tag = tag[0].upper() + tag[1:]
	return tag


def edge_cases(tag):
	"""Handle edge cases such as roman numerals and parantheses."""
	# Roman numerals
	if any(word.strip(':') in ROMAN_NUMS for word in tag.split()):
		for word in tag.split():
			if word.strip(':') in ROMAN_NUMS:
				tag = tag.replace(word, word.upper())
	# Parentheses, colons, ellipses
	matches = re_parens.findall(tag)
	for match in matches:
		tag = tag.replace(match, match.upper())
	# Underscores (title likely pulled from file name)
	while '_' in tag:
		c = input(f'What character should replace the _ in {tag}? ')
		tag = tag.replace('_', c, 1)
	return tag


def main():
	base = Path('/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy')
	modified = 0
	for artist in base.iterdir():
		artist_path = base/artist
		print(artist.name)
		for album in artist_path.iterdir():
			album_path = artist_path/album
			if album.is_file():
				album = make_unknown(artist_path/album)
			if album.name != 'Unknown Album':
				print(' ', album.name)
			modified += modify_album(album_path)
	return modified


if __name__ == '__main__':
	modified = main()
	# modified = modify_album('/Users', 'tmcou', 'Downloads', individual=True)
	print(f'\nModified {modified} songs.')
