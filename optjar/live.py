#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 - capture market data every 1 minute on Monday - Friday
 - only perform task if current time between 9.00 and 17.00
 - files will appear in price-data/ folder 
 
Created on Dec 4, 2018

@author: chayapan
'''

from datetime import datetime
import time

def priceCaptureThread(thcap_latest_prices):
    while True:
        ts = datetime.now()
        weekend = ts.weekday() in [5,6] # now is during weekend?
        print "Current Hour:", ts.hour, "Before 5PM?:", ts.hour < 17, "After 9AM?:", ts.hour >= 9, "Weekend?:", weekend
        if ts.hour >= 9 and ts.hour < 17 and not weekend:
            try:
                print "Archive price data."
                thcap_latest_prices.capture()
            except Exception as e:
                print e
            time.sleep(60) # sleep 1 minute
        else:
            time.sleep(60 * 15) # sleep 15 minutes during off-hours
            