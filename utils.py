from smtplib import SMTP
from email.mime.text import MIMEText

def market_status():
    """Either market is open or market is closed.
        Open:
            10 AM to 4.30 PM on weekday
    """
    is_open = False
    return is_open


def send_message(name, contact, message):
    name = name.encode('utf8','ignore')
    contact = contact.encode('utf8','ignore')
    message = contact.encode('utf8','ignore')
    # me == the sender's email address
    # you == the recipient's email address
    server = 'mail.tegancloud.com'
    me = "optjar@disqrete.com"
    you = "boss@chayapan.com"
    message = """Name: {}\nContact: {}\nMessage:\n{}""".format(name,contact,message)
    msg = MIMEText(message)
    msg['Subject'] = 'thaimarketcap.com - question from: %s (%s)' % (name, contact)
    msg['From'] = me
    msg['To'] = you
    print "Connecting..."
    USERNAME = 'chayapan@tegancloud.com'
    PASSWORD = 'ticonder0G@'
    conn = SMTP(server)
    conn.set_debuglevel(True)
    conn.starttls() # need this or error with AUTH not support
    conn.login(USERNAME, PASSWORD)
    print "Logged In."
    try:
        conn.sendmail(me, [you], msg.as_string())
        print "Message Sent"
    except Exception as e:
        print e
    finally:
        conn.quit()


if __name__ == '__main__':
    send_message(name="test", contact="test@test.com", message="Hey")
