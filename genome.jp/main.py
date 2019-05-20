#!/usr/bin/python3

"""
parse data from www.genome.jp
"""

import sys
from get_page import request_page
from parse import Parser
import os

#global vars: common url part for genome.jp website
url_base = 'https://www.genome.jp'
url_part_info = '/dbget-bin/www_bget?'
url_part_graph = '/kegg-bin/show_pathway?'


def parse_metabolite(code):
    url = url_base +  url_part_info + code
    formula = ''
    html = request_page(url)
    parsed = Parser(html)
    text = parsed.get_soup().get_text().split('\n')
    for i in range(len(text)):
        if text[i] == 'Formula':
            formula = text[i+1].replace('\n', '')
    return formula        
    

def parse_pathway(code):

    class Parser_genome_website(Parser):
        
        def parse_graph_pathway_metabolites(self):
            circles = self.get_soup().findAll('area',
                                   attrs={'shape': "circle"})
            circle_titles = list(map(lambda x: x.get('title'), circles))
            circle_hrefs = list(map(lambda x: x.get('href'), circles))
    
            def process_string(title):
                title = title.replace('(','')
                title = title.replace(')','')
                title = title.split(' ',1)
                return title
     
            metabolite_codes = list(map(process_string, circle_titles))
            for i in range(len(metabolite_codes)):
                metabolite_codes[i].append(circle_hrefs[i])
            return metabolite_codes
        
    url = url_base +  url_part_graph + code
    html = request_page(url)
    parsed = Parser_genome_website(html)
    metabolites = parsed.parse_graph_pathway_metabolites()
    #<font class="title3"><b>Pentose phosphate pathway - Reference pathway</b></font>
    title = parsed.get_soup().find('font',
                           attrs={'class': "title3"})
    title = title.get_text().split('-')[0]
    
    metabolites_found = []
    codes_found = []
    for mol in metabolites:
        formula = ''
        
        code = mol[0]
        if code not in codes_found: 
            codes_found.append(code)
            name = mol[1]
            print(name)
            formula = parse_metabolite(code)
            if formula == '':
                with open('error_log', 'a') as file:
                    file.write('formula not found: ' + code + ', ' + name + '\n')
            else: 
                metabolites_found.append([name, formula, title])
    return metabolites_found


if __name__ == '__main__':
    if len(sys.argv) == 2:
        code = sys.argv[1]
        metabolites_found = parse_pathway(code)
    else:
        code = 'map00030'
        metabolites_found = parse_pathway(code)
        
        file_results = 'results.csv'
        
        #export to csv:
        if not os.path.exists(file_results):
            with open(file_results, 'a') as csvfile:
                csvfile.write('Molecule,Formula,Process' + '\n')
        for row in metabolites_found:
            with open(file_results, 'a') as csvfile:
                    csvfile.write(','.join(row) + '\n')

