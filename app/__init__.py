from flask.ext.mail import Mail
from flask import Flask

app = Flask(__name__)
mail = Mail(app)
