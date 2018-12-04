"""
Collect most recent data from SetTrade.com web site on all stocks.
Save to JSON file.
"""

import requests
from bs4 import BeautifulSoup
import os, os.path
from datetime import datetime
import json
from multiprocessing import Pool

WORKERS = 30
ts = datetime.now()

dataFolder = os.path.join(os.path.abspath("."),"""issue-detail""")
baseURL = """http://www.settrade.com"""
startPage = """http://www.settrade.com/C13_MarketSummary.jsp?detail=STOCK_TYPE&order=N&market=SET&type=S"""
snapshotFile = os.path.join(dataFolder, "snapshot" + ts.strftime("%Y%m%d_%H%M") + ".dat")

r = requests.get(startPage)
# check content received
print r.status_code

# Prepare directory
if not os.path.exists(dataFolder):
    os.mkdir(dataFolder)

# Save the index page
indexFile = os.path.join(dataFolder, "market" + ts.strftime("%Y%m%d_%H%M") + ".html")
with open(indexFile, "w") as f:
    f.write(r.content)

# load into BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

def get_quotes_links(soup):
    links = soup.find_all("a")
    for link in links:
        if link.has_attr('href'):
            if link.attrs['href'].startswith("/C13_FastQuote_Main.jsp"):
                print link.get_text()
                print link.attrs
                yield link

def download_factsheet(symbol):
    # 1. collect factsheet
    factsheet_url = """https://www.set.or.th/set/factsheet.do?symbol=%s&ssoPageId=3&language=th&country=TH""" % symbol
    r = requests.get(factsheet_url)
    print "Factsheet:", factsheet_url, r.status_code
    issueFactsheet = os.path.join(dataFolder, ts.strftime("%Y%m%d_") + "factsheet_%s_" % symbol + ".html")

    # load into BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')
    soup.find("")
    with open(issueFactsheet, "w") as f:
        f.write(r.content)

def download_quote_page(args):
    symbol, link = args[0], args[1]
    # 2. collect quote page
    quote_url = link['href']
    r = requests.get(baseURL + quote_url)
    print "Quote:", quote_url, r.status_code
    issueQuote = os.path.join(dataFolder, ts.strftime("%Y%m%d_") + "quote_%s_" % symbol + ".html")
    with open(issueQuote, "w") as f:
        f.write(r.content)


print datetime.now().strftime("%Y%m%d_%H%M")

market_data = {}
market_data['src'] = startPage
market_data['ts'] = str(ts)
market_data['data'] = {}

symbols = []
quotes = []

for link in get_quotes_links(soup):
    print link
    print link.parent.parent.get_text()

    raw_data_cell = link.parent.parent.get_text().split('\n')
    raw_data_cell.remove('') # realign cell. Remove empty element.
    symbol = raw_data_cell[0].encode('ascii',errors='ignore') # Remove non ascii chars
    if '<' in symbol: # for flaged stocks
        symbol = symbol[:symbol.find('<')]
        n = raw_data_cell[0].encode('ascii',errors='ignore')
        flag = n[n.find('<'):]

    price_latest = raw_data_cell[4]

    market_data['data'][symbol] = {}
    market_data['data'][symbol]['symbol'] = symbol
    market_data['data'][symbol]['price_latest'] = price_latest

    symbols.append(symbol)
    quotes.append((symbol,link))

# Do download in parallel
p = Pool(WORKERS)
p.map(download_factsheet, symbols)

p = Pool(WORKERS)
p.map(download_quote_page, quotes)

# Save the data file in json
dataFile = os.path.join(dataFolder, "market" + ts.strftime("%Y%m%d_%H%M") + ".json")
with open(dataFile, "w") as f:
    f.write(json.dumps(market_data, sort_keys=True, indent=4, separators=(',', ': ')))

