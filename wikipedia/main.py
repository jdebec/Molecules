#!/usr/bin/python3

"""
    parse_page.py

    1 parse process page and get all wikipedia links
    2 initialize csv file for results
    3 iterate through all linked wikipedia pages found.
    If an info box is found in this page:
        3.1 extract it with pandas
        3.2 try to extract Cheminal formula row
        3.3 else, try to extract Formula row
        3.4 try to extract mesh (full chemical name)
        3.5 if a chemical formula is found, export result into csv
"""

from get_page import request_page
from get_page import get_page_html
from parse_page import get_internal_links
from parse_page import parse_info_box
import os.path
import sys

if __name__ == '__main__':

    if len(sys.argv) == 3:
        lang = sys.argv[0]
        process = sys.argv[1]        
    else:
        lang = 'en'
        process = 'Pentose_phosphate_pathway'
    
    #1 parse process page and get all wikipedia links
    page = request_page(lang, process)
    page = get_page_html(page)
    links = get_internal_links(page)
    links = list(set(links))
    links = [link.replace('/wiki/', '') for link in links]
    links = [link for link in links if '.' not in link]
    
    #2 initialize csv file for results
    file_results = 'results.csv'
    if not os.path.exists(file_results):
        with open(file_results, 'a') as csvfile:
            csvfile.write('Molecule, Formula, MeSH, Process' + '\n')
    
    #3 iterate through all other wikipedia pages found
    for link in links:
        print(link)
        page = request_page(lang, link)
        html = get_page_html(page) 
        table = parse_info_box(html)
        
        #3.1 if an info box is found, extract it with pandas
        if table is not None:
            chemical_formula = ''
            mesh = ''
            
            #3.2 try to extract Cheminal formula row
            req = table[table[0] == "Chemical formula"]
            if len(req) > 0:
                    chemical_formula = req[1].item()
            
            #3.3 else, try to extract Formula row
            else :
                req = table[table[0] == "formula"]
                if len(req) > 0:
                        chemical_formula = req[1].item()
                        
            #3.4 try to extract mesh (full name)
            req = table[table[0] == "MeSH"]
            if len(req) > 0:
                    mesh = req[1].item()
            
            #3.4 if a chemical formula is found, export result into csv
            if chemical_formula != '':
                results_line = [link, chemical_formula, mesh, process]
                with open(file_results, 'a') as csvfile:
                    csvfile.write(', '.join(results_line) + '\n')
                    
            else:
                with open('no_formula', 'a') as file:
                    file.write(link + '\n')
                    
        else:
            with open('no_info_box', 'a') as file:
                file.write(link + '\n')