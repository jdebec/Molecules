#!/usr/bin/python3

"""
    get_page.py
"""

import requests
import sys

def request_page(lang='en',
                 title="Main_Page",
                 verbose = False):
    
    S = requests.Session()
    URL = "https://{}.wikipedia.org/w/api.php".format(lang)
    PARAMS = {
        'action': "parse",
        'page': title,
        'format': "json"
    }
    if verbose:print(URL, PARAMS)
    try:
        R = S.get(url=URL, params=PARAMS)
        if R.ok:
            return(R.json())
    
    except:
        error_msg = 'request failed: ' + str(title)+ ':' + str(lang)
        if verbose: print(error_msg)
        else:
            with open('error_log', 'a') as file:
                file.write(error_msg + '\n')
        return {}
    
def get_page_html(json_response, verbose =False):
    if 'parse' in json_response.keys():
        html = json_response['parse']['text']['*']
    
    elif 'error' in json_response.keys():
        html = ''
        error_msg = 'wikipedia page error: ' + json_response['error']['info']
        if verbose: print(error_msg)
        else:
            with open('error_log', 'a') as file:
                file.write(error_msg + '\n')
    
    return html
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        lang = sys.argv[0]
        page = sys.argv[1]
        verbose = sys.argv[2]
        print(request_page(lang, page, verbose))
        
    else:
        lang = 'en'
        page = '6-phosphoglucono-%CE%B4-lactone'
        
        page = request_page(lang, page)
        print(page)
        page = get_page_html(page)
