#!/usr/bin/python3

"""
    parse_page.py
"""

from bs4 import BeautifulSoup
import regex as re
import pandas as pd
from get_page import request_page
from get_page import get_page_html

def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.findAll('a')
    return [link.get('href') for link in links]

def get_internal_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.findAll('a', attrs={'href': re.compile("wiki")})
    return [link.get('href') for link in links]

def get_tables(html):
    return pd.read_html(html)

def parse_info_box(html):
    soup = BeautifulSoup(html, 'html.parser')
    box = soup.findAll("table", {"class": "infobox bordered"})
    if len(box) == 1:        
        return get_tables(str(box[0]))[0]
    else:
        return None

if __name__ == '__main__':
    lang = 'en'
    page = 'Fructose_6-phosphate'
    
    page = request_page(lang, page)
    html = get_page_html(page)
    box = parse_info_box(html)
    print(box)
    

