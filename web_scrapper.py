from bs4 import BeautifulSoup
from selenium import webdriver


class WebScraper:
    __driver = ""
    __html = ""
    __soup = ""

    def __init__(self, url):
        self.__driver = webdriver.PhantomJS()
        self.__driver.get(url)
        self.__html = self.__driver.execute_script('return document.documentElement.outerHTML')
        self.__soup = BeautifulSoup(self.__html, 'html.parser')

    def update_page(self):
        self.__html = self.__driver.execute_script('return document.documentElement.outerHTML')
        self.__soup = BeautifulSoup(self.__html, 'html.parser')

    def grab_html_full(self):
        self.update_page()
        return self.__html

    def grab_tag_from_html(self, tag, attrs={}):
        self.update_page()
        return self.__soup.find_all(tag, attrs=attrs)
