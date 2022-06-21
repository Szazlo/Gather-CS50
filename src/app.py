from itertools import product
from pipes import Template
from urllib import response
from flask import Flask, render_template, request, make_response, redirect, session, url_for, g
from flask_session import Session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import DecimalField
from forms import *
from database import get_db, close_db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
#from helpers import login_required

app = Flask(__name__)
Session(app)

db = sqlite3.connect('app.db')

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "Password123"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

user_id = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """Welcome page"""
    if request.method == "GET":
    # Render dashboard if user is logged in

        print("Checking for session id")
        print(session["username"])
        try:
            if session["username"]:
                return redirect("/dashboard")
        except:
            print("No user logged in")
            return render_template("welcome.html")
    else:
        # Redirect to register page.
        return redirect("/register")


            
@app.route("/dashboard")
def dashboard():
    """Dashboard page"""
    
    return render_template("dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""
    # Define the form 
    form = registerForm()

    if request.method == "GET":
        return render_template("register.html", form=form)

    else:
 
        form = registerForm()
        if form.validate_on_submit():
            # Get form data
            firstName = str(form.firstName.data)
            lastName = str(form.lastName.data)
            username = db.execute("SELECT username FROM users WHERE username = ?", (form.username.data,)).fetchall()

            if len(username) == 1:
                return render_template("register.html", form=form, error="Username already exists")
            
            username = str(form.username.data)

            email = db.execute("SELECT email FROM users WHERE email = ?", (form.email.data,)).fetchall()
            if len(email) == 1:
                return render_template("register.html", form=form, error="Email already exists")

            email = str(form.email.data)

            password = form.password.data
            # Hash password
            hashed_password = str(generate_password_hash(password))
            # Insert user into database
            db.execute("INSERT INTO users (username, email, password, firstName, lastName) VALUES (?, ?, ?, ?, ?)", 
                                          (username, email, hashed_password, firstName, lastName))
            db.commit()
            print((db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchall())["username"])
            session["username"] = (db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchall())["username"]
            return redirect("/")

