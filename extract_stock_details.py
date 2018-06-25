#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Collect most recent data from SetTrade.com web site on all stocks.
Save to JSON file.
"""

import requests
from bs4 import BeautifulSoup
import os, os.path
from datetime import datetime
import json
import re
from multiprocessing import Pool

WORKERS = 30
ts = datetime.now()
dataFolder = os.path.join(os.path.abspath("."),"""issue-detail""")


def get_files():
    count = 0
    for f in os.listdir(dataFolder):
        if "quote" in f and count < 1000:
            count += 1
            yield os.path.join(dataFolder, f)

for f in get_files():
    with open(f,"r") as f0:
        soup = BeautifulSoup(f0.read(), 'html.parser')

        match_div = soup.find('h2')
        print match_div.get_text()

        match_div = soup.findAll('div', {"class": "row content-box-stt"})
        for d in match_div:
            dat = d.get_text().strip()
            dat = dat[:dat.find("NVDR")+30]
            dat = dat.replace('\n', '')
            print dat
            pttr = re.compile(r'\d+(?:,\d+.\d+)?')
            m = pttr.findall(dat) 
            if m :
                print m
