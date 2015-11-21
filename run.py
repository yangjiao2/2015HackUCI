# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, jsonify, render_template, request, url_for
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
BASEURL = "jpatrickpark.com"

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)
cron = Scheduler(daemon=True)
cron.start()

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=str)
    #print generate_removal_url(a,b)
    response = urllib2.urlopen("https://www.reg.uci.edu/perl/WebSoc?YearTerm=2016-03&ShowFinals=1&ShowComments=1&CourseCodes={}".format(str(a)))
    html = response.read()
    found = html.find("FULL")
    if found == -1:
        waitlist = html.find("Waitl")
        if waitlist == -1:
            if html.find("OPEN") != -1:
                return jsonify(result="The class {} is OPEN! Go to Webreg and enroll now!".format(str(a)))
            else:    
                return jsonify(result="The course {} does not exist!".format(str(a)))
        else:
            return jsonify(result="The class {} is FULL, but the WAITLIST is still open! Go ahead and get in the waitlist!".format(str(a)))
    else:
        #add to database here
        return jsonify(result="The class {} is FULL! We will email you when the class becomes available.".format(str(a)))

def generate_removal_url(course,user):
    '''generate a link that calls remove_pair() function when clicked'''
    return '/_remove_pair?courseID={}&userID={}'.format(str(course),user)

@app.route('/_remove_pair', methods=['GET'])
def remove_pair():
    '''Removes a pair when a user clicks a specific link'''
    '''Must error-check'''
    '''127.0.0.1:5000/_remove_pair?courseID=VVV&userID=XXX'''
    print request.args.get('courseID')
    print request.args.get('userID')
    return render_template('thanks.html')

@cron.interval_schedule(minutes=1)
def check_courses():
    '''goes through the database every minute, updates status, and send emails if any class "becomes available".'''
    #send_email(29090,'jungkyup')
    pass

#@app.route('/_send_email')
def send_email(courseID,userID):
    msg = Message('Your class {} became available! from MyUCIClassisFull'.format(str(courseID)), sender=ADMINS[0], recipients=[userID+'@uci.edu'])
    #msg.body = 'Your class {} became available!'.format(str(courseID))
    msg.html = 'Your class <strong> {} </strong> became available! <p> Go enroll in your class on WebReg. <p> If you succeeded in enrolling in the class and want to stop getting this email, click this link to <a href = "{}">unsubscribe</a>. '.format(str(courseID), BASEURL+generate_removal_url(courseID,userID))
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=33507)
