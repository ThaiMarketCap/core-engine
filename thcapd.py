#!/usr/bin/env python
"""
 - capture data every 30 seconds
 - only perform task if current time between 9.00 and 17.00
 - serve Flask app in separate thread
"""

import subprocess
from datetime import datetime
import time
from flask import Flask, session, redirect, url_for
from flask import send_file, request, send_from_directory, render_template
import thread
from random import randint
from utils import send_message

app = Flask(__name__, static_url_path='', template_folder="www")

@app.route("/")
def main():
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    market_status = "Market is closed."
    n1, n2 = randint(0,20), randint(0,99)
    captcha_challenge = "What is the value of {} + {}?".format(n1,n2)
    captcha_answer = n1 + n2
    return render_template('index.html', current_time = current_time,
                                         market_status = market_status,
                                        captcha_answer = captcha_answer,
                                        captcha_challenge = captcha_challenge)

@app.route("/comment", methods=['GET', 'POST'])
def comment():
    print "Comment received:", request.values
    v = request.values
    send_message(name=v['name'], contact=v['contact'], message=v['message'])
    print "Sent email"
    return redirect(url_for('main'))

@app.route('/<path:image>.jpg')
def send_image(image):
    """Serv JPEG files from 'www' directory"""
    try:
        image = image + ".jpg"
        return send_from_directory('www', image)
    except Exception as e:
        return str(e)
@app.route("/changes-to-trade-value")
def changes2val():
    try:
        return send_file('www/today.html')
    except Exception as e:
	    return str(e)

@app.route("/price-to-marketcap")
def price2mkcap():
    try:
        return send_file('www/price2mkcap.html')
    except Exception as e:
	    return str(e)
@app.route('/data/<path:path>')
def send_js(path):
    return send_from_directory('price-indices', path)

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
