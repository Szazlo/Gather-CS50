from itertools import product
from pipes import Template
import re
from urllib import response
from functools import wraps
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
# from helpers import login_required

app = Flask(__name__)

db = sqlite3.connect('app.db', check_same_thread=False)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "(.Y.)__Xyz143Babs"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    ''' Decorator to check if user is logged in '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session["email"]:
                print("User is logged in")
        except KeyError:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
def index():
    """Welcome page"""
    if request.method == "POST":
            # Redirect to dashboard if the user has just registered
            return redirect("/dashboard")

    if request.method == "GET":
    # Render dashboard if user is logged in

        print("Checking for session id")
        try:
            if session["id"]:
                print("Session id found")
                print(session["id"])
                return redirect("/dashboard")
        except:
            print("No user logged in")
            return render_template("welcome.html")

            
@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard page"""
    # Get user's id from session
    user_id = session["email"]
    # Get user's name from database
    username = db.execute("SELECT username FROM users WHERE email = ?", (user_id,)).fetchone()[0]

    return render_template("dashboard.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""
    # Define the form 
    form = registerForm()

    if request.method == "GET":
        return render_template("register.html", form=form)

    else:
 
        # form = registerForm()
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
            print("Hashing password")
            hashed_password = str(generate_password_hash(password))
            # Insert user into database
            print("Inserting user into database")
            db.execute("INSERT INTO users (username, email, password, firstName, lastName) VALUES (?, ?, ?, ?, ?)", 
                                          (username, email, hashed_password, firstName, lastName))
            print("Committing changes to database")
            db.commit()
            
            # Add user to session
            session["email"]= form.email.data

            return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def Login():
    form = loginForm()

    if request.method == "POST":
        
        if form.validate_on_submit():
            # Get user's id from database
            print("Submitted data")
            email = str(form.email.data)
            print(f"Email is {email}")
            password = str(form.password.data)
            print(f"Password is {password}")
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            print(user)

            # Check if user exists
            if len(user) == 1:
                # Check if password is correct
                if check_password_hash(user[0][2], password):
                    # Add user to session
                    print("Added user to session")
                    session["email"]= email
                    print("Redirecting to dashboard")
                    return redirect("/")
                else:
                    return render_template("login.html", form=form, error="Incorrect password")
            else:
                return render_template("login.html", form=form, error="User does not exist")

    if request.method == "GET":
        return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    """Logout page"""
    # Remove user from session
    session.pop("email", None)
    return redirect("/")