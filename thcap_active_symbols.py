"""
Collect most recent data from SetTrade.com web site on all stocks.
Save to JSON file.
"""

import requests
from bs4 import BeautifulSoup
import os, os.path
from datetime import datetime
import json

ts = datetime.now()

dataFolder = os.path.join(os.path.abspath("."),"""market-data""")
baseURL = """http://www.settrade.com"""
startPage = """http://www.settrade.com/C13_MarketSummary.jsp?detail=STOCK_TYPE&order=N&market=SET&type=S"""
snapshotFile = os.path.join(dataFolder, "snapshot" + ts.strftime("%Y%m%d_%H%M") + ".dat")

r = requests.get(startPage)
# check content received
print r.status_code
# print r.content[:100]

# Save the index page
indexFile = os.path.join(dataFolder, "market" + ts.strftime("%Y%m%d_%H%M") + ".html")
with open(indexFile, "w") as f:
    f.write(r.content)

# load into BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

# print soup

def get_quotes_links(soup):
    links = soup.find_all("a")
    for link in links:
        if link.has_attr('href'):
            if link.attrs['href'].startswith("/C13_FastQuote_Main.jsp"):
                print link.get_text()
                print link.attrs
                yield link

print datetime.now().strftime("%Y%m%d_%H%M")

market_data = {}
market_data['src'] = startPage
market_data['ts'] = str(ts)
market_data['symbols'] = []
market_data['active'] = []
market_data['flagged'] = []

for link in get_quotes_links(soup):
    print link
    print link.parent.parent.get_text()

    raw_data_cell = link.parent.parent.get_text().split('\n')
    raw_data_cell.remove('') # realign cell. Remove empty element.
    symbol = raw_data_cell[0].encode('ascii',errors='ignore') # Remove non ascii chars
    price_latest = raw_data_cell[4]
    ok = True
    if '<' in symbol: # for flaged stocks
        symbol = symbol[:symbol.find('<')]
        ok = False
        n = raw_data_cell[0].encode('ascii',errors='ignore')
        flag = n[n.find('<'):]

    # add to all symbols
    market_data['symbols'].append(symbol)

    if ok:
        issue = {}
        issue['symbol'] = symbol
        issue['price_latest'] = price_latest
        market_data['active'].append(issue)
    else:
        issue = {}
        issue['symbol'] = symbol
        issue['flag'] = flag
        issue['price_latest'] = price_latest
        market_data['flagged'].append(issue)

# Save the data file in json
dataFile = os.path.join(dataFolder, "symbols" + ts.strftime("%Y%m%d") + ".json")
with open(dataFile, "w") as f:
    f.write(json.dumps(market_data, sort_keys=True, indent=4, separators=(',', ': ')))
