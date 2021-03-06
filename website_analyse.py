import bs4 as bs
import urllib.request
import urllib.parse
import validators
import string
# note that package lxml also needs to be installed to let bs4 work in this code


class WebData:
	""" Represents website's object
		Connects to the site in __init__

		url: given website's url
		agent: 'user_agent' or 'robot'
		have_data: boolean, False if got error during connection
		http_error: handles http error if found
		error: string version of an error if that occured during connection

		url_bytes: opened site or None if connection failed
	"""


	def __init__(self, url, agent='robot'):
		self.url = url
		self.agent = agent
		self.have_data = False
		self.http_error = None
		self.error = None
		self.url_bytes = None


	def __str__(self):
		return f"url: {self.url}\n"\
			   f"agent: {self.agent}\n"\
			   f"have_data: {self.have_data}\n"\
			   f"http_error: {self.http_error}\n"\
			   f"error: {self.error}"


	def open_url(self):
		"""
		    Scraps the website as a python bot or imitates user agent
		    if no error occured it is considered that data has been obtained

		    self.http_error is saved only if 'http error' is found
		    every error is saved in self.error
		"""
		try:
			if self.agent == 'robot':
				url_bytes = urllib.request.urlopen(self.url)
				
			elif self.agent == 'user_agent':
				headers = {}
				headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 " \
										"(KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
				req = urllib.request.Request(self.url, headers=headers)
				url_bytes = urllib.request.urlopen(req)
			self.url_bytes = url_bytes
			self.have_data = True
		except urllib.error.HTTPError as e:
			e = str(e).lower()
			index = e.find('http error')
			if index >= 0 and len(e) > index+5:
				self.http_error = e[index: len('http error')+4]
			self.error = e
		except Exception as e:
			self.error = str(e)


class WebAnalyse:
	"""
	Analyses given website in order to check frequency of used keywords

	webdata: WebData object
	sauce: plain text from url_bytes
	soup: bs4.BeautifulSoup object; structured website's code
	keywords: set of keywords from metatag; empty list if not found
	p: generator with text from p tags
	keywords_frequency: histogram dictionary
	"""
	def __init__(self, webdata):
		self.webdata = webdata
		self.sauce = webdata.url_bytes.read()
		self.soup = bs.BeautifulSoup(self.sauce, 'lxml')
		self.keywords_tag = self.check_for_keywords()
		self.keywords = []
		if self.keywords_tag:
			self.keywords = set(WebAnalyse.keywords_from_metatag(self.keywords_tag))
		self.p_text = (p.text for p in self.soup.find_all('p'))
		self.keywords_frequency = {keyword.lower(): 0 for keyword in self.keywords}
		self.count_keywords()


	def __str__(self):
		if self.keywords_frequency:
			if len(self.keywords_frequency) < 10:
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


	def check_for_keywords(self):
		""" Looks for meta tag with 'name': 'keywords'
			if not found analyses all meta tags with 'name'
			to find 'keywords' written with upper letters

			if it was found then extract keywords from meta tag
			else returns an empty list
		"""
		meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
		if meta_keywords is None:
			for meta in self.soup.find_all('meta'):
				try:
					if meta.attrs['name'].lower() == 'keywords':
						return meta
				except KeyError:
					continue


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


	@staticmethod
	def keywords_from_metatag(metatag):
		"""
			Looks for 'content' tag in given meta tag and separates its contents by ',' and clears spaces
		"""
		for tag in metatag.attrs:
			if tag.lower() == 'content':
				return [key.strip(' ') for key in metatag[tag].split(',')]


def main():
	url = 'https://www.w3schools.com'
	data = WebData(url)
	data.open_url()
	if data.have_data:
		webanalyse = WebAnalyse(data)
		print(webanalyse.__repr__())
	else:
		print(data)
		

if __name__ == '__main__':
	main()