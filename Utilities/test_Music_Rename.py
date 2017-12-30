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

class TestRename(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		os.chdir(base)
		os.makedirs('Test Artist/Test Album')
		os.chdir('Test Artist')
		with open('Lonely Song.txt', 'w'):
			pass
		os.chdir('Test Album')
		with open('Test song 1.txt', 'w'):
			pass
		with open('Test song 2.txt', 'w'):
			pass
		with open('Test song 3.txt', 'w'):
			pass
		with open('Test song 4.txt', 'w'):
			pass

	@classmethod
	def tearDownClass(cls):
		os.chdir(base)
		rmtree('Test Artist')

	def test_modify_song(self):
		pass

	def test_make_unknown(self):
		Music_Rename.make_unknown(base, 'Test Artist', 'Lonely Song.txt')
		os.chdir(os.path.join(base, 'Test Artist', 'Unknown Album'))
		self.assertTrue(os.path.isfile('Lonely Song.txt'))


if __name__ == '__main__':
	unittest.main()
