#!/usr/bin/python3

"""
    parse.py
    parser class:
        handles beautiful soup request
        handles pandas table extraction
"""

from bs4 import BeautifulSoup
import pandas as pd


class Parser():
    
    def __init__(self, html_code):
        self.html = html_code
        self.soup = False
        self.links = False
        self.tables = False
    
    def get_soup(self, parser = 'html.parser'):
        if not self.soup:
            self.soup = BeautifulSoup(self.html, parser)
        return self.soup

    def get_links(self):
        if not self.links:
            links = self.get_soup().findAll('a')
            self.links = [link.get('href') for link in links]
        return self.links
    
    def get_tables(self):
        if not self.tables:
            tables = pd.read_html(self.html)
            self.tables = tables
        return self.tables

if __name__ == '__main__':
    with open('response.html', 'r') as file:
        html = file.read()
    
    page = Parser(html)
    print(page.get_links())
    print(page.get_tables())
    

