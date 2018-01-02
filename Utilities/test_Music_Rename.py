"""
	Testing site for the Music_Rename module.
	Tim Coutinho
"""

import unittest
from pathlib import Path
from shutil import rmtree

from mutagen.easyid3 import EasyID3

import Music_Rename

base = Path('/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy/Test Artist')
files = {'1.txt': ['i am easy', 'I Am Easy'],
		 '2.txt': ['How about: a colon?', 'How About: A Colon?'],
		 '3.txt': ['now some() (of) These)', 'Now Some() (Of) These)'],
		 '4.txt': ['..ooh, a forward/slash!', '..Ooh, a Forward / Slash!'],
		 '5.txt': ['edge (de): iv ......cases', 'Edge (De): IV ......Cases'],
		 '6.txt': ['futuresex / lovesounds', 'FutureSex / LoveSounds'],
		 '7.txt': ['id', 'ID']}

class TestRename(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		album = base/'Test Album'
		album.mkdir(parents=True)
		with (album.parent/'Lonely Song.txt').open('w'):
			pass
		for key in files:
			with (album/key).open('w'):
				pass


	def test_modify_tag(self):
		for file in (base/'Test Album').iterdir():
			new = Music_Rename.modify_tag(files[file.name][0])
			self.assertEqual(files[file.name][1], new)

	def test_make_unknown(self):
		song_path = base/'Lonely Song.txt'
		Music_Rename.make_unknown(song_path)
		self.assertTrue(
			((song_path.parent/'Unknown Album'/song_path.name).is_file()))


	@classmethod
	def tearDownClass(cls):
		rmtree(base)


if __name__ == '__main__':
	unittest.main()
