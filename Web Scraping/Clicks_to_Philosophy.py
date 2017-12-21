'''
	Determines how many clicks it takes to get to the
	Wikipedia page for Philosphy, given a starting article.
	WIP
	Tim Coutinho
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen

def main():
	while True:
		try:
			raw = input('Article: ')
			article = '/wiki/' + raw.replace(' ', '_')
			score = calculate(article)
		except TypeError:
			print('Disambiguation page reached or no links found, try again.')
		except Exception:
			print('Article does not exist, try again.')
		else:
			if score is None:
				print('''It looks like there are no clickable
						 links in paragraphs on that page.''')
			elif score >= 0:
				print(f'''It takes {score} steps to
						  get from {raw} to Philosophy.''')
				break

def calculate(article):
	if article == '/wiki/Philosophy':
		return 0
	if article == '/wiki/Alphabet':
		print('''You've reached Alphabet, which means
				 you're stuck in a loop, unfortunately.''')
		return -1000
	elif article == '/wiki/Branch':
		print('''You've reached Branch, which means
			     you're stuck in a loop, unfortunately.''')
		return -1000
	with urlopen(f'https://en.wikipedia.org{article}') as url:
		site = BeautifulSoup(url, 'lxml')
	print(site.h1.text)  # The name of the article as displayed on the page
	for paragraph in site.find('div', class_='mw-parser-output').find_all('p'):
		for link in paragraph.find_all('a', recursive=False):
			if ('cite_note' not in link['href']
							  and link['href'] is not article):
				# Don't want citations or same article links
				return calculate(link['href']) + 1
		
if __name__ == '__main__':
	main()