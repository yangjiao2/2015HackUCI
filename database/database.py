# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

FULL = 0
OPEN = 1
import os, sqlite3
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
conn = None

# # create our little application :)
# app = Flask(__name__)

# # Load default config and override config from an environment variable
PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE = 'hackuci.db'
SCHEMA = 'schema.sql'
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, DATABASE),
#     DEBUG=True,
#     SECRET_KEY='development key',
#     USERNAME='admin',
#     PASSWORD='default'
# ))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)



def connect_db():
    """Connects to the specific database."""
    global conn
    conn = sqlite3.connect(DATABASE)
    return conn


def init_db():
    """Initializes the database."""
    global conn
    with sqlite3.connect(DATABASE) as conn:
        with open(SCHEMA, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
    return conn


# # @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables."""
#     init_db()
#     print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    global conn
    if not os.path.exists(DATABASE):
        init_db()
    if not conn:
        connect_db()
    return conn
 


# @app.teardown_appcontext
def close_db():
    """Closes the database again at the end of the request."""
    if conn:
        conn.close()


#@app.route('/classes')
def get_courses():
    # try to get all the course_id
    print '=> execute get_courses'
    db = get_db()
    cur = db.cursor().execute('SELECT course_id FROM courses ORDER BY course_id')
    courses_tuple = cur.fetchall()
    # return render_template('show_classes.html', courses=courses)
    course_list = [course[0] for course in courses_tuple]
    return course_list

def get_courses_tuple():
    # try to get all the course_id
    print '=> execute get_courses'
    db = get_db()
    cur = db.cursor().execute('SELECT * FROM courses ORDER BY course_id')
    courses_tuple = cur.fetchall()
    return courses_tuple


#@app.route('/add', methods=['POST'])
def add_following_course(user_email, course_id):
    # check if user_email is in the db.users, if not in, add a new user
    # check if course_id is in the db.courses, if not in , add a new course
    # add the pair to db.follows
    print '=> execute add_following_course'
    db = get_db()
    user_id = 0
    cur = db.cursor().execute('SELECT user_id FROM users WHERE email = ?', [user_email])
    user_exist_result = cur.fetchall()
    if user_exist_result == []:
        cur = db.cursor().execute('SELECT max(user_id) FROM users')
        max_id = cur.fetchone()
        if max_id == None:
            max_id = 0
        else:
            max_id = max_id[0]

        db.cursor().execute('INSERT INTO users (user_id , email) VALUES (?, ?)', [max_id + 1, user_email])
        db.commit()

        cur = db.cursor().execute('SELECT * FROM users')
        user_id = max_id + 1
    else:
        user_id = user_exist_result[0][0]  


    cur = db.cursor().execute('SELECT course_id FROM courses WHERE course_id = ?', [course_id])
    course_exist_result = cur.fetchall()
    if course_exist_result == []:
        db.cursor().execute('INSERT INTO courses (course_id, status) VALUES (?, ?)', [course_id, FULL])
        db.commit()

    cur = db.cursor().execute('SELECT follower_user_id, followed_course_id FROM follows WHERE follows.follower_user_id = ? AND follows.followed_course_id = ?', [user_id, course_id])
    if cur.fetchall() == [] and user_id != 0:
        db.cursor().execute('INSERT INTO follows(follower_user_id, followed_course_id) VALUES (?, ?)', [user_id, course_id])
        db.commit()

    return 'success'


# @app.route('/add', methods=['POST'])
def delete_following_course(user_email, course_id):
    # check if user_email is in the db.users, if not in, add a new user
    # check if course_id is in the db.courses, if not in , add a new course
    # add the pair to db.follows
    print '=> execute delete_following_course'
    db = get_db()
    user_id = 0

    cur = db.cursor().execute('SELECT user_id FROM users WHERE email = ?', [user_email])
    check_user_exist_result = cur.fetchall()
    if check_user_exist_result == []:
        return 'fail'
    else:
        user_id = check_user_exist_result[0][0]

    cur = db.cursor().execute('SELECT follower_user_id, followed_course_id FROM follows WHERE follows.follower_user_id = ? AND follows.followed_course_id = ?', [user_id, course_id])
    follow_exist_result = cur.fetchall()
    if follow_exist_result == []:
        return 'fail'
    else:
        cur = db.cursor().execute('DELETE FROM follows WHERE follows.follower_user_id = ? AND follows.followed_course_id = ?', [user_id, course_id])
        db.commit()

    cur = db.cursor().execute('SELECT follower_user_id, followed_course_id FROM follows WHERE follows.follower_user_id = ?', [user_id])
    user_exist_result = cur.fetchall()
    if user_exist_result == []:
        db.cursor().execute('DELETE FROM users WHERE user_id = ?', [user_id])
        db.commit()



    cur = db.cursor().execute('SELECT follower_user_id, followed_course_id FROM follows WHERE follows.followed_course_id = ?', [course_id])
    course_exist_result = cur.fetchall()
    if course_exist_result == []:
        db.cursor().execute('DELETE FROM courses WHERE course_id = ?', [course_id])
        db.commit()

    return 'success'


def get_notified_users(course_id):
    # get all the user's email that follows changed_course_id
    db = get_db()
    cur = db.cursor().execute('SELECT users.email FROM users, follows WHERE follows.followed_course_id = ? AND follows.follower_user_id = users.user_id', [course_id])
    notified_users_tuple = cur.fetchall()
    if notified_users_tuple == []:
        return []

    notified_users_list = [email[0] for email in notified_users_tuple]
    return notified_users_list

def is_status_changed(course_id, changed_status):
    # get the course's status by given course_id
    # return True or False whether the course_id is changed
    # True if it changes, False if it is not changed
    db = get_db()
    prev = db.cursor().execute('SELECT * FROM courses WHERE course_id = ?', [course_id])
    course = prev.fetchone()
    print '==', course[0], course[1]
    db.execute('UPDATE courses SET status = ? WHERE course_id = ?', [changed_status, course_id])
    return changed_status != course[1]


