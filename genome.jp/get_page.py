#!/usr/bin/python3

"""
    get_page.py
    request get to the specified url
"""

import requests
import sys

def request_page(url, verbose = False):
    try:
        R = requests.get(url)
        if R.ok:
            return(R.text)
    except:
        error_msg = 'request failed: ' + str(url)
        if verbose: print(error_msg)
        else:
            with open('error_log', 'a') as file:
                file.write(error_msg + '\n')
        return None
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[0]
        
    else:
        url = 'https://biocyc.org/ECOLI/NEW-IMAGE?type=PATHWAY&object=PENTOSE-P-PWY'
        
    
    page = request_page(url, verbose = False)
    with open('response.html', 'w') as file:
        file.write(page)