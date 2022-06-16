from itertools import product
from pipes import Template
from urllib import response
from flask import Flask, render_template, request, make_response, redirect, session, url_for, g
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import DecimalField
from forms import *
from database import get_db, close_db
from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "Password123"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.teardown_appcontext(close_db)
Session(app)

@app.route("/")
def index():
    return render_template("index.html")