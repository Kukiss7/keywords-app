import bs4 as bs
import re
import string
import abc


class GeneralTag(metaclass=abc.ABCMeta):

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



class TagsData:
    """

    """
    def __init__(self, soup, tag_type):
        self.soup = soup
        self.tag_type = tag_type
        self.tags_set = self.find_tags()
        self._data = None


    def find_tags(self):
        return self.soup.find_all(self.tag_type.name, attrs=self.tag_type.attrs)


    @property
    def data(self):
        if not self._data:
            data = []
            for tag in self.tags_set:
                for word in self.tag_type.extract_data(tag):
                    data.append(word)
            self._data = data
        return self._data
    
