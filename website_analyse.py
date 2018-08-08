import bs4 as bs
import urllib.request
import urllib.parse
import validators
import string
import requests
# note that package lxml also needs to be installed to let bs4 work in this code


class WebData:
	""" Represents website's object
		Connects to the site in __init__

		url: given website's url
		agent: 'user_agent' or 'robot'

		url_bytes: opened site
		sauce: plain text from url_bytes
		soup: bs4.BeautifulSoup object; structured website's code
		keywords: set of keywords from metatag; empty list if not found
	"""
	def __init__(self, url, agent='robot'):
		self.url = url
		self.agent = agent
		self.url_bytes = self.open_url()
		self.sauce = self.url_bytes.read()
		self.soup = bs.BeautifulSoup(self.sauce, 'lxml')
		self.keywords = self.check_for_keywords()
		site_map_url = None
		site_map_sauce = None

	def __str__(self):
		return f"url: {self.url}\nagent: {self.agent}\nkeywords: {self.keywords}"

	def open_url(self, given_url=None):
		"""scraps the website as a python bot or imitates user agent
		   returns site as bytes
		"""
		assert self.agent == 'robot' or self.agent == 'user_agent', "agent must have one of two given values: " \
																	"'robot' or 'user_agent'"
		if given_url is None:
			given_url = self.url
		if self.agent == 'robot':
			return urllib.request.urlopen(given_url)
		elif self.agent == 'user_agent':
			headers = {}
			headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 " \
									"(KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
			req = urllib.request.Request(given_url, headers=headers)
			return urllib.request.urlopen(req)

	def check_for_keywords(self):
		""" Looks for meta tag with 'name': 'keywords'
			if not found analyzes all meta tags with 'name'
			to find 'keywords' written with upper letters

			if it was found then extract keywords from meta tag
			else returns an empty list
		"""
		meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
		if meta_keywords is None:
			for meta in self.soup.find_all('meta'):
				try:
					if meta.attrs['name'].lower() == 'keywords':
						meta_keywords = meta
				except KeyError:
					continue
		if meta_keywords:
			return set(WebData.keywords_from_metatag(meta_keywords))
		else:
			return []

	def check_for_site_map(self):
		# should check if it is a main site
		"""
		Check if given domain has its site map

		It is not used for now
		"""
		endings = ['sitemap.xml', 'sitemap']
		for ending in endings:
			full_link = urllib.parse.urljoin(self.url, ending)
			try:
				sauce = self.open_url(given_url=full_link)
				if sauce.getcode() == 200:
					self.site_map_url = full_link
					self.site_map_sauce = sauce
			except urllib.error.HTTPError:
				continue

	def site_map_urls_gen(self):
		"""return a generator with links"""
		if self.site_map_url.endswith('.xml'):
			for data in self.site_map_soup.find_all('url'):
				for element in data.text.split():
					if validators.url(element):
						yield element
		else:
			for data in self.site_map_soup.find_all("div"):
				yield data.get('href')

	@staticmethod
	def keywords_from_metatag(metatag):
		"""
			Looks for 'content' tag in given meta tag and separates its contents by ',' and clears spaces
		"""
		try:
			for tag in metatag.attrs:
				if tag == 'content':
					return [key.strip(' ') for key in metatag[tag].split(',')]
		except AttributeError as e:
			print(f"Keywords not found probably, error: {e}\n{metatag}")


class WebAnalyse:
	"""
	Analyzes given website in order to check frequency of used keywords

	webdata: WebData object
	p: generator with text from p tags
	keywords_frequency: histogram dictionary
	"""
	def __init__(self, webdata):
		self.webdata = webdata
		self.p_text = (p.text for p in webdata.soup.find_all('p'))
		self.keywords_frequency = {keyword.lower(): 0 for keyword in self.webdata.keywords}
		self.count_keywords()

	def __str__(self):
		if self.keywords_frequency:
			if len(self.keywords_frequency) < 8:
				lines_dist = '\n\n'
			else:
				lines_dist = '\n'
			res = ''
			res = res + f"Checked url: {self.webdata.url}\n\nKeywords found on the site:\n\n"
			for keyword, value in self.keywords_frequency.items():
				res = res + f"{keyword}: {value}{lines_dist}"
			return res
		else:
			return "Found no keywords"

	def __repr__(self):
		res = ''
		res += str(self.webdata) + '\n'
		res += str(self.keywords_frequency) + '\n'
		return res

	def count_keywords(self):
		"""
			Searches keywords in text from <p> paragrapghs
			Iterates through text, lowers words and eliminates punctuation signs 
			to check words with keywords

			Updates self.keyword_frequency dictionary
		"""
		for text in self.p_text:
			for word in text.split():
				word = word.strip(string.punctuation).lower()
				if word in self.keywords_frequency:
					self.keywords_frequency[word] += 1

def main():
	url = 'https://www.w3schools.com'
	data = WebData(url)
	webanalyse = WebAnalyse(data)
	print(webanalyse.__repr__())

if __name__ == '__main__':
	main()




