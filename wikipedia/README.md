# Molecules

Small scope project to extract molecules involved in paths associated to their chemical formulas. The data is extracted from scrapping wikipedia pages

## Procedure description

    1 parse process page and get all wikipedia links
    2 initialize csv file for results
    3 iterate through all linked wikipedia pages found.
    If an info box is found in this page:
        3.1 extract it with pandas
        3.2 try to extract Cheminal formula row
        3.3 else, try to extract Formula row
        3.4 try to extract mesh (full chemical name)
        3.5 if a chemical formula is found, export result into csv
        

## Built With

* Python3
* Pandas
* BeautifulSoup4


## Command line

python main.py
* ARG1: language ('en')
* ARG2: wikipedia page (the last part of the page url)

For instance:
```
python main.py en Pentose_phosphate_pathway
```
