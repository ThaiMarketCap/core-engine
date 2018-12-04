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
if not os.path.exists(dataFolder):
    os.mkdir(dataFolder)
data = {}

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
        name_th = match_div.get_text()
        symbol = name_th.split('-')[0].strip()

        data[symbol] = {}
        data[symbol]['name_th'] = name_th

        match_div = soup.findAll('div', {"class": "row content-box-stt"})
        for d in match_div:
            dat = d.get_text().strip()
            dat = dat[:dat.find("NVDR")+30]
            dat = dat.replace('\n', '')
            print dat
            print "=" * 20

            # Extract dividend
            dat = dat.encode("utf8")
            kw = """ตอบแทนเงินปันผล"""
            pos = dat.find(kw)
            focus = dat[pos+len(kw):pos+len(kw)+20]
            pos2 = focus.find('%')
            res = focus[1:pos2]

            try:
                dividend_pct = float(res.strip())
                print dividend_pct
                data[symbol]['dividend_pct'] = dividend_pct
            except ValueError as e:
                print "No Dividend Data"

            # Registered shares
            #   วนหุ้นจดทะเบียน 308,676,462   ราคาสูงสุด/
            kw_s = """หุ้นจดทะเบียน"""
            kw_t = """ราคาสูงสุด"""
            pos1 = dat.find(kw_s)
            pos2 = dat.find(kw_t)
            focus = dat[pos1+len(kw_s):pos2]
            focus = focus.strip()
            focus = focus.replace(',', '') # remove ,

            try:
                registered_shares = float(focus)
                print registered_shares
                data[symbol]['registered_shares'] = registered_shares
            except ValueError as e:
                print "No Registered Shares Data"
            
            # Book value
            #    คาปิดต่อมูลค่าตามบัญชี 3.75   หุ้นปันผล (
            kw_s = """ปิดต่อมูลค่าตามบัญชี"""
            kw_t = """หุ้นปันผล"""
            pos1 = dat.find(kw_s)
            pos2 = dat.find(kw_t)
            focus = dat[pos1+len(kw_s):pos2]
            focus = focus.strip()
            focus = focus.replace(',', '') # remove ,

            try:
                price_to_book_value = float(focus)
                print price_to_book_value
                data[symbol]['price_to_book'] = price_to_book_value
            except ValueError as e:
                print "No P/B Data"
       
            # Price/Earning
	    #    ราคาปิดต่อกำไรสุทธิ 10.18   ผลตอบแทนเงินปันผล 
            kw_s = """รสุทธิ"""
            kw_t = """ผลตอบแทนเงินปันผล"""
            pos1 = dat.find(kw_s)
            pos2 = dat.find(kw_t)
            focus = dat[pos1+len(kw_s):pos2]
            focus = focus.strip()
            focus = focus.replace(',', '') # remove ,
            try:
                price_to_earning = float(focus)
                print price_to_earning
                data[symbol]['price_to_earning'] = price_to_earning
            except ValueError as e:
                print "No P/E Data"

	    # Earning per shares
	    #   ไรต่อหุ้น (บาท) 0.22   เงินปันผลต่อหุ้น (
            kw_s = """ไรต่อหุ้น (บาท)"""
            kw_t = """เงินปันผลต่อหุ้น"""
            pos1 = dat.find(kw_s)
            pos2 = dat.find(kw_t)
            focus = dat[pos1+len(kw_s):pos2]
            focus = focus.strip()
            focus = focus.replace(',', '') # remove ,
            try:
                eps = float(focus)
                print eps
                data[symbol]['earnings_per_share'] = eps
            except ValueError as e:
                print "No EPS Data"

out = {'data': data}
with open("price-indices/securities.json", "w") as f:
     f.write(json.dumps(out))
