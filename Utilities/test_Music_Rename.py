"""
	Testing site for the Music_Rename module.
	Tim Coutinho
"""

import unittest
import os
from shutil import rmtree

from mutagen.easyid3 import EasyID3

import Music_Rename


class TestRename(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		os.chdir('/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy')
		os.makedirs('Test Artist/Test Album')
		os.chdir('Test Artist/Test Album')
		with open('Test song1.mp3', 'w'):
			pass
		with open('Test song2.mp3', 'w'):
			pass
		with open('Test song3.mp3', 'w'):
			pass
		with open('Test song4.mp3', 'w'):
			pass

	@classmethod
	def tearDownClass(cls):
		os.chdir('/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy')
		rmtree('Test Artist')

	def test_modify_song(self):
		pass

	def test_make_unknown(self):
		pass


if __name__ == '__main__':
	unittest.main()
