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
from database import *

FULL = 0
OPEN = 1
get_db()
BASEURL = "https://myuciclassisfull.mybluemix.net"

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
                return jsonify(signal="y",result="The class {} is OPEN! Go to Webreg and enroll now!".format(str(a)))
            else:    
                return jsonify(signal="r",result="The course {} does not exist!".format(str(a)))
        else:
            return jsonify(signal="y",result="The class {} is FULL, but the WAITLIST is still open! Go ahead and get in the waitlist!".format(str(a)))
    else:
        add_pair(a,b)
        return jsonify(signal="g",result="The class {} is FULL! We will email you when the class becomes available.".format(str(a)))

def generate_add_url(course,user):
    '''generate a link that calls add_pair() function when clicked'''
    return '/_add_pair?courseID={}&userID={}'.format(str(course),user)

def generate_removal_url(course,user):
    '''generate a link that calls remove_pair() function when clicked'''
    return '/_remove_pair?courseID={}&userID={}'.format(str(course),user)

def add_pair(courseID,userID):
    add_following_course(userID,int(courseID))

@app.route('/_add_pair', methods=['GET'])
def add_pair_from_link():
    '''Removes a pair when a user clicks a specific link'''
    '''Must error-check'''
    '''Do something about these two values with database'''
    add_pair(request.args.get('courseID'),request.args.get('userID'))
    return render_template('you_are_back_on.html')

@app.route('/_remove_pair', methods=['GET'])
def remove_pair():
    '''Removes a pair when a user clicks a specific link'''
    '''Must error-check'''
    '''Do something about these two values with database'''
    uID = request.args.get('userID')
    cID = int(request.args.get('courseID'))
    delete_following_course(uID,cID)
    send_email(cID,uID,1)
    return render_template('thanks.html')

@cron.interval_schedule(minutes=1)
def check_courses():
    '''goes through the database every minute, updates status, and send emails if any class "becomes available".'''
    # I iterate through the courses and send email for everyone
    courseList = get_courses()
    for i in courseList:
        response = urllib2.urlopen("https://www.reg.uci.edu/perl/WebSoc?YearTerm=2016-03&ShowFinals=1&ShowComments=1&CourseCodes={}".format(str(i)))
        html = response.read()
        found = html.find("FULL")
        is_open = (found == -1)
        if is_status_changed(i,is_open):
            userList = get_notified_users(i)
            for user in userList:
                send_email(i,user,0)

#@app.route('/_send_email')
def send_email(courseID,userID,is_unsubscribe):
    
    #msg.body = 'Your class {} became available!'.format(str(courseID))
    if is_unsubscribe:
        msg = Message('Your have unsubscribed from MyUCIClassisFull for class {}!'.format(str(courseID)), sender=ADMINS[0], recipients=[userID+'@uci.edu'])
        msg.html = 'Your notification for class number <strong> {} </strong> is now unsubscribed! <p> If you believe this is a mistake, click this link to <a href="{}">subscribe</a> again!'.format(str(courseID), BASEURL+generate_add_url(courseID,userID))
    else:
        msg = Message('Your class {} became available! from MyUCIClassisFull'.format(str(courseID)), sender=ADMINS[0], recipients=[userID+'@uci.edu'])
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
    app.run()
