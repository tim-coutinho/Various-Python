"""
	Shows the top 10 links in the specified subreddit using BeautifulSoup.
	Tim Coutinho
"""

import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen

MAX_POSTS = 10

def main():
	subreddit = input('Subreddit: ')
	csv_file = open(f'top{str(MAX_POSTS)}{subreddit.capitalize()}.csv', 'w', newline='')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Title', 'Link'])
	with urlopen(f'https://www.reddit.com/r/{subreddit}/') as url:
		site = BeautifulSoup(url, 'lxml')
	i = 0

	posts = site.find_all('div', onclick='click_thing(this)')	# Only the actual posts in the subreddit
	print(f"\nCurrent top posts in {posts[0]['data-subreddit']}:\n")

	for post in posts:
		try:
			if post.find('span', class_='stickied-tagline') is None:	# Is not a stickied post
				title, link = (post.find('p', class_='title').a.text, post['data-url'])
				if '/r/' in link:
					link = 'https://www.reddit.com' + link
				print(title, link)
				csv_writer.writerow([title, link])
				i += 1
				if i == MAX_POSTS:
					return
		except Exception as e:
			pass
	if i == 0:	# Somehow all stickied posts or all errors
		print('No links found.')

	csv_file.close()
		
if __name__ == '__main__':
	main()