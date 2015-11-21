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
from config import ADMINS
from threading import Thread
import atexit
from apscheduler.scheduler import Scheduler
# use apscheduler version 2.1.2
# pip install apscheduler==2.1.2

FULL = 0
OPEN = 1

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)
cron = Scheduler(daemon=True)
cron.start()

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=str)
    print b
    response = urllib2.urlopen("https://www.reg.uci.edu/perl/WebSoc?YearTerm=2016-03&ShowFinals=1&ShowComments=1&CourseCodes={}".format(str(a)))
    html = response.read()
    found = html.find("FULL")
    if found == -1:
        waitlist = html.find("Waitl")
        if waitlist == -1:
            if html.find("OPEN") != -1:
                return jsonify(result="The class is OPEN! Go to Webreg and enroll now!")
            else:    
                return jsonify(result="The course does not exist!")
        else:
            return jsonify(result="The class is FULL, but the WAITLIST is still open! Go ahead and get in the waitlist!")
    else:
        #add to database here
        return jsonify(result="The class is FULL! We will email you when the class becomes available.")

def generate_removal_url():
    '''generate a link that calls remove_pair() function when clicked'''
    pass

@app.route('/_...')
def remove_pair():
    '''Removes a pair when a user clicks a specific link'''
    '''Must error-check'''
    pass

@cron.interval_schedule(minutes=1)
def check_courses():
    '''goes through the database every minute, updates status, and send emails if any class "becomes available".'''
    pass
    #send_email(29090)

#@app.route('/_send_email')
def send_email(courseID,ListofEmails):
    msg = Message('Your class {} became available!'.format(str(courseID)), sender=ADMINS[0], recipients=ListofEmails)
    msg.body = 'Your class {} became available!'.format(str(courseID))
    #msg.html = '<b>HTML</b> body'
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
