"""
searchpypi.py - opens in the browser several search results 
from https://pypi.org
"""

import sys
import time
import webbrowser
import requests

from bs4 import BeautifulSoup


PYPI = 'https://pypi.org'
SELECTOR = '.unstyled > li > a'
# number of search results to open in new tab
NUM_OPEN = 5

search = ' '.join(sys.argv[1:]) 

if not search:
    print("Search query not found! Try again.")
    sys.exit()
print("Searching...")

search_link = PYPI + '/search/?q=' + search

pypi_response = requests.get(search_link)
pypi_response.raise_for_status()

pypi_soup = BeautifulSoup(pypi_response.text, 'html.parser')

top_results = pypi_soup.select(SELECTOR)[:NUM_OPEN]

for res in top_results:
    res_link = PYPI + res.get('href')
    print("Opening ", res_link)
    time.sleep(0.5)
    webbrowser.open(res_link)
