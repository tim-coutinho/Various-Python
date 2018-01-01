"""
	Testing site for the Music_Rename module.
	Tim Coutinho
"""

import unittest
import os
from shutil import rmtree

from mutagen.easyid3 import EasyID3

import Music_Rename

base = '/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy'
files = {'1.txt': ['i am easy', 'I Am Easy'],
		 '2.txt': ['How about: a colon?', 'How About: A Colon?'],
		 '3.txt': ['now some() (of) These)', 'Now Some() (Of) These)'],
		 '4.txt': ['..ooh, a forward/slash!', '..Ooh, a Forward / Slash!'],
		 '5.txt': ['edge (wait): iv ......cases', 'Edge (Wait): IV ......Cases'],
		 '6.txt': ['futuresex / lovesounds', 'FutureSex / LoveSounds'],
		 '7.txt': ['id', 'ID']}

class TestRename(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		os.chdir(base)
		os.makedirs('Test Artist/Test Album')
		os.chdir('Test Artist')
		with open('Lonely Song.txt', 'w'):
			pass
		os.chdir('Test Album')
		for key in files.keys():
			with open(key, 'w'):
				pass


	def test_modify_tag(self):
		os.chdir(os.path.join(base, 'Test Artist', 'Test Album'))
		for file in os.listdir():
			new = Music_Rename.modify_tag(files[file][0])
			self.assertEqual(files[file][1], new)

	def test_make_unknown(self):
		Music_Rename.make_unknown(base, 'Test Artist', 'Lonely Song.txt')
		os.chdir(os.path.join(base, 'Test Artist', 'Unknown Album'))
		self.assertTrue(os.path.isfile('Lonely Song.txt'))


	@classmethod
	def tearDownClass(cls):
		os.chdir(base)
		rmtree('Test Artist')


if __name__ == '__main__':
	unittest.main()
