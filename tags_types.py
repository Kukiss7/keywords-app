import bs4 as bs
import re
import string
import abc


class GeneralTag(metaclass=abc.ABCMeta):
    """
        Base class for custom Tags classes


        arbitrary attributes that need too be provided:
        
        property - name: string
        property - attrs: dictionary to put in soup.find_all method
        static method - extract_data: should return needed list of objects
    """


    # name and attrs are variables to search for meta tag
    @property
    @abc.abstractmethod
    def name(self, value):
        self.name = value


    @property
    @abc.abstractmethod
    def attrs(self, value):
        self.attrs = value


    @staticmethod
    @abc.abstractmethod
    def extract_data(tag):
        pass


class PTag(GeneralTag):
    """
        Configuration to search for data in <p> tags
    """

    name = 'p'
    attrs = {}


    @staticmethod
    def extract_data(tag):
        text = tag.text
        words_list = []
        for word in text.split():
            words_list.append(word.strip(string.punctuation).lower())       
        return words_list


class KeywordsTag(GeneralTag):
    """
        Configuration to search for keywords from meta tag
    """

    # attrs' expression looks for pair 'name':'keywords' 
    # where keywords is case insensitive 
    name = 'meta'
    attrs = {'name':re.compile("^keywords$", re.I)}


    @staticmethod
    def extract_data(tag):
        try:
            content = tag.attrs['content']
        except KeyError:
            return
        kw_list = (keyword.strip().lower() for keyword in content.split(','))     
        return kw_list



class TagData:
    """
        Gathers information from bs.BeautifulSoup object
        based on given tag type

        soup: bs.BeautifulSoup object
        tag_type: given tag properties
        tag_parts_set: set of tags
        property _data: list - gathered data extracted with tag_type.extract_data() 
    """
    def __init__(self, soup, tag_type):
        self.soup = soup
        self.tag_type = tag_type
        self.tag_parts_set = self.find_tags()
        self._data = None


    def find_tags(self):
        return self.soup.find_all(self.tag_type.name, attrs=self.tag_type.attrs)


    @property
    def data(self):
        if not self._data:
            data = []
            for tag in self.tag_parts_set:
                for word in self.tag_type.extract_data(tag):
                    data.append(word)
            self._data = data
        return self._data
    
