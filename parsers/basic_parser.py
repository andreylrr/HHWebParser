from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
        Abstract class for classes that will be used for parsing
        HTML pages from the Head Hunter website.
    """
    @abstractmethod
    def parse(self, html_page, data_dict):
        print("Parsing in Base class")
