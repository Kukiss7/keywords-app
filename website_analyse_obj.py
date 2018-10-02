import bs4 as bs
import urllib.request
import urllib.parse
import validators
import string
import re
from collections import Counter
from tags_types import TagData, KeywordsTag, PTag

# note that package lxml also needs to be installed to let bs4 work in this code


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 " \
    "(KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"


class WebBytes:
    """ 
        Represents website's object
        Connects to the site in __init__

        url: given website's url
        use_user_agent: boolean 
        have_data: boolean, False if got error during connection
        http_error: handles http error if found
        error: string version of an error if that occured during connection

        url_bytes: opened site or None if connection failed
    """
    def __init__(self, url, use_user_agent=False):
        self.url = url
        self.use_user_agent = use_user_agent
        self.http_error = None
        self.error = None
        self.request_headers = {}
        self._set_request_headers()
        self.sauce = ''


    def __str__(self):
        return f"url: {self.url}\n"\
               f"use_user_agent: {self.use_user_agent}\n"\
               f"have_data: {self.have_data}\n"\
               f"http_error: {self.http_error}\n"\
               f"error: {self.error}"


    def _set_request_headers(self):
        headers = {}
        if self.use_user_agent:
            headers['User-Agent'] = USER_AGENT
        self.request_headers = headers


    def open_url(self):
        """
            Scraps the website as a python bot or imitates user agent
            if no error occured it is considered that data has been obtained

            self.http_error is saved only if 'http error' is found
            every error is saved in self.error
        """
        req = urllib.request.Request(self.url, headers=self.request_headers)
        try:
            with urllib.request.urlopen(req) as url_bytes:
                self._save_sauce(url_bytes)
        except urllib.error.HTTPError as e:
            self.http_error = e
        except Exception as e:
            self.error = str(e)


    def _save_sauce(self, url_bytes):
        self.sauce = url_bytes.read()
            


class WebData():
    """
        Analyses given website, checks for metatag with keywords and searches p tags from body
        webdata: WebData object
        sauce: plain text from url_bytes
        soup: bs4.BeautifulSoup object; structured website's code
    """
    def __init__(self, sauce, parser='lxml'):
        self.parser = parser
        self.sauce = sauce
        self.soup = bs.BeautifulSoup(self.sauce, self.parser)


class UrlValidation:
    """
        Validates given url and makes sure to output an url that starts with 'http' or 'https'

        input_url: str; provided url
        validator: str; kind of validators that input_url has passed through 'url' or 'domain'
        validation: boolean;
        http_url: output url with made sure for 'http://' at the beginning
    """
    def __init__(self, input_url):
        self.input_url = input_url
        self.validation = self.validate_url()
        self.http_url = self.set_http_url()


    def validate_url(self):
        """
            Validates given url
        """

        return validators.url(self.input_url) or validators.domain(self.input_url)


    def set_http_url(self):
        """
            Takes self.url and returns new one with added 'http://' to url 
            if 'http://' or 'https://' is not present
        """

        if self.input_url[:7] == 'http://' or self.input_url[:8] == 'https://':
            return self.input_url
        else:
            return 'http://' + self.input_url


def count_items(items):
    return Counter(items)


def filter_by_container(source, target):
    t_set = set(target)
    res = [element for element in source if element in t_set]
    return res


def main():
    url = 'https://www.w3schools.com/'
    data = WebBytes(url, use_user_agent=True)
    data.open_url()


if __name__ == '__main__':
    url = 'https://w3schools.com/'
    web = WebBytes(url, use_user_agent=True)
    web.open_url()
    sauce = web.sauce
    soup = WebData(sauce).soup
    kw_cont = TagData(soup, KeywordsTag)
    p_cont = TagData(soup, PTag)


    # kw_tags = find_tags(soup, 'meta', attrs={'name':re.compile("^keywords$", re.I)})
    # kw_tag
    # keywords = kw_tag.get('content')
    # kw_list = [key.strip() for key in keywords.split(',')]
