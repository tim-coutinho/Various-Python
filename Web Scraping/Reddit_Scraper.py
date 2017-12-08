"""
	Shows the top 10 links in the specified subreddit using BeautifulSoup.
	Tim Coutinho
"""

import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen

MAX_POSTS = 10

def main():
	subreddit = input("Subreddit: ")
	with urlopen(f'https://www.reddit.com/r/{subreddit}/') as url:
		site = BeautifulSoup(url, 'lxml')
	i = 0
	print(f"\nCurrent top posts in {subreddit}:\n")
	for post in site.find_all('div', onclick="click_thing(this)"):
		try:
			if post.find('span', class_='stickied-tagline') is None:
				print(post.find('p', class_='title').a.text, post['data-url'])
				i += 1
				if i == MAX_POSTS:
					return
		except Exception as e:
			pass
	if i == 0:
		print('No links found.')
		
if __name__ == '__main__':
	main()