# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#@app.route('/classes')
def get_courses():
    # try to get all the course_id
    db = get_db()
    cur = db.execute('select course_id from courses order by id')
    courses = cur.fetchall()
    # return render_template('show_classes.html', courses=courses)
    return courses

#@app.route('/add', methods=['POST'])
def add_following_course(user_email, course_id):
    # check if user_email is in the db.users, if not in, add a new user
    # check if course_id is in the db.courses, if not in , add a new course
    # add the pair to db.follows
    db = get_db()
    db.execute('select email from users where email = ?', user_email)
    if db.fetchone() == []:
        db.execute('SELECT max(id) FROM users')
        max_id = db.fetchone()[0]
        db.execute('INSERT INTO users (, text) VALUES (?, ?)', [max_id, user_email])
        db.commit()

    db.execute('SELECT email FROM course WHERE course = ?', course_id)
    if db.fetchone() == []:
        db.execute('INSERT INTO course WHERE ')
        max_id = db.fetchone()[0]
        db.execute('insert into users (, text) values (?, ?)', [max_id, user_email])
        db.commit()



    db.execute('insert into entries (user_id, email) values (?, ?)', [])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


# @app.route('/add', methods=['POST'])
def delete_following_course(user_email, course_id):
    # check if user_email is in the db.users, if not in, add a new user
    # check if course_id is in the db.courses, if not in , add a new course
    # add the pair to db.follows

