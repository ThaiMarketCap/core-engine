#!/usr/bin/env python
"""
 - capture data every 30 seconds
 - only perform task if current time between 9.00 and 17.00
 - serve Flask app in separate thread
"""

import subprocess
from datetime import datetime
import time
import thread

from optjar.live import priceCaptureThread
from optjar.www import app
import thcap_latest_prices

def flaskThread():
    app.run(host='0.0.0.0', port=5000)
    
def do_compute():
    try:
        import compute_indices
        reload(compute_indices)
        print "Get Data Done."
        import plot_market
        reload(plot_market)
        print "Plot Data Done."
        import plot_price2mkcap
        reload(plot_price2mkcap)
        print "Plot 2 Done."
    except Exception as e:
        print e

if __name__ == '__main__':
    s = 0
    thread.start_new_thread(flaskThread,()) # start Flask
    thread.start_new_thread(priceCaptureThread,(thcap_latest_prices,)) # start Price capture

    while True:
        ts = datetime.now()
        # print "DoW:", ts.weekday() # Friday = 4
        weekend = ts.weekday() in [5,6] # now is during weekend?
        print "Current Hour:", ts.hour, "Before 5PM:", ts.hour < 17, "After 9AM:", ts.hour >= 9, "Weekend?:", weekend
        if ts.hour >= 9 and ts.hour < 17 and not weekend:
            print s, datetime.now()
            s += 1
            do_compute()
            time.sleep(30) # sleep 30 seconds
        else:
            time.sleep(60 * 15) # sleep 15 minutes during off-hours
