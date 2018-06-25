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
market_data['rank'] = {}
market_data['data'] = {}

for link in get_quotes_links(soup):
    print link
    print link.parent.parent.get_text()

    raw_data_cell = link.parent.parent.get_text().split('\n')
    raw_data_cell.remove('') # realign cell. Remove empty element.
    symbol = raw_data_cell[0].encode('ascii',errors='ignore') # Remove non ascii chars
    price_open = raw_data_cell[1]
    price_high = raw_data_cell[2]
    price_low = raw_data_cell[3]
    price_latest = raw_data_cell[4]
    price_change = raw_data_cell[5]
    pct_change = raw_data_cell[6]
    price_bid = raw_data_cell[7]
    price_offer = raw_data_cell[8]
    shares_volume = raw_data_cell[9]
    shares_value_thb  = raw_data_cell[10]

    quote_url = link.attrs['href']
    print "Quote:", quote_url
    try:
        price_latest = float(price_latest.replace(',',''))
    except ValueError:
        price_latest = 0
    try:
        shares_volume = float(shares_volume.replace(',',''))
    except ValueError:
        shares_volume = 0
    try:
        shares_value_thb = float(shares_value_thb.replace(',','')) * 1000.0
    except ValueError:
        shares_value_thb = 0

    market_data['data'][symbol] = {}
    market_data['data'][symbol]['symbol'] = symbol
    market_data['data'][symbol]['price_open'] = price_open
    market_data['data'][symbol]['price_low'] = price_low
    market_data['data'][symbol]['price_high'] = price_high
    market_data['data'][symbol]['price_latest'] = price_latest
    market_data['data'][symbol]['price_change'] = price_change
    market_data['data'][symbol]['pct_change'] = pct_change
    market_data['data'][symbol]['price_bid'] = price_bid
    market_data['data'][symbol]['price_offer'] = price_offer
    market_data['data'][symbol]['shares_volume_qty'] = shares_volume
    market_data['data'][symbol]['shares_value_thb'] = shares_value_thb


    market_data['data'][symbol]['market_cap'] = shares_volume * price_latest

# Save the data file in json
dataFile = os.path.join(dataFolder, "rank" + ts.strftime("%Y%m%d_%H%M") + ".json")
with open(dataFile, "w") as f:
    f.write(json.dumps(market_data, sort_keys=True, indent=4, separators=(',', ': ')))
