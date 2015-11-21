# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, jsonify, render_template, request
import urllib2
from flask.ext.mail import Mail,Message
from config import ADMINS, MAIL_HOST,MAIL_PORT,MAIL_HOSTNAME,MAIL_PASSWORD,MAIL_USE_TLS,MAIL_USE_SSL
from threading import Thread

app = Flask(__name__)
mail = Mail(app)

@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    response = urllib2.urlopen("https://www.reg.uci.edu/perl/WebSoc?YearTerm=2016-03&ShowFinals=1&ShowComments=1&CourseCodes={}".format(str(a)))
    html = response.read()
    found = html.find("FULL")
    if found == -1:
        waitlist = html.find("Waitl")
        if waitlist == -1:
            send_email()
            return jsonify(result="OPEN")
        else:
            return jsonify(result="Waitl")
    else:
        return jsonify(result="FULL")

#@app.route('/_send_email')
def send_email():
    msg = Message('Your class became available!', sender=ADMINS[0], recipients=ADMINS)
    msg.body = 'Your class _ became available!'
    msg.html = '<b>HTML</b> body'
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
