from itertools import product
from pipes import Template
import re
from urllib import response
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render
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
from helpers import isRoleBasedEmail

app = Flask(__name__)

db = sqlite3.connect('app.db', check_same_thread=False)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "( . Y . )__Xyz143Babs"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config["RECAPTCHA_PUBLIC_KEY"] = "6LeThr0gAAAAAKyhPwM3Xp8t4hMYM_2alO8xV1v-"
# app.config["RECAPTCHA_PRIVATE_KEY"] = "6LeThr0gAAAAALbqm5g5F5KT17iG-ynxPT8-5oA_" # use with captcha v2

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
            if session["email"]:
                print("Session id found")
                print(session["email"])
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

    # Check if user has is verified
    username = db.execute("SELECT username FROM unverifiedUsers WHERE email = ?", (user_id,)).fetchone()
    if username:
        # The user is not verified and needs to verify their account to see the real dashboard
        return render_template("dashboard.html", username="unverified user")

    # Get user's name from the main database
    username = db.execute("SELECT username FROM users WHERE email = ?", (user_id,)).fetchone()

    #Failsafe for if the user is not in the database but the session is still active
    if username == None:
        return redirect("/logout")

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
                form.username.errors.append("Username already exists")
                return render_template("register.html", form=form)
            
            username = str(form.username.data)

            if isRoleBasedEmail(form.email.data):
                form.email.errors.append("Email is not valid")
                return render_template("register.html", form=form)

            email = db.execute("SELECT users.email FROM users JOIN unverifiedUsers ON users.email = unverifiedUsers.email WHERE users.email = ?", 
                              (form.email.data,)).fetchall()
            if len(email) != 0:
                form.email.errors.append("Email already exists")
                return render_template("register.html", form=form)

            email = str(form.email.data)

            password = form.password.data
            passwordErrors = 0
            if not any(char.isdigit() for char in password):
                passwordErrors += 1
                form.password.errors.append("Password must contain at least one number")
            if not any(char.isalpha() for char in password):
                passwordErrors += 1
                form.password.errors.append("Password must contain at least one letter")
            if not any(char.isupper() for char in password):
                passwordErrors += 1
                form.password.errors.append("Password must contain at least one uppercase letter")
            if not any(char.islower() for char in password):
                passwordErrors += 1
                form.password.errors.append("Password must contain at least one lowercase letter")
            if not any(not char.isalnum() for char in password):
                passwordErrors += 1
                form.password.errors.append("Password must contain a symbol")

            if passwordErrors > 0:
                return render_template("register.html", form=form)
                
            if form.confirmPassword.data != password:
                form.confirmPassword.errors.append("Passwords do not match")
                return render_template("register.html", form=form)
            
            # Hash password
            hashed_password = str(generate_password_hash(password))
            # Insert user into database
            print("Inserting user into database")
            db.execute("INSERT INTO unverifiedUsers (username, email, password, firstName, lastName) VALUES (?, ?, ?, ?, ?)", 
                                          (username, email, hashed_password, firstName, lastName))
            print("Committing changes to database")
            db.commit()
            
            # Add user to session
            session["email"]= form.email.data

            # Redirect to email verification page
            return redirect("/emailVerification")

@app.route("/login", methods=["GET", "POST"])
def Login():
    form = loginForm()

    if request.method == "POST":
        
        if form.validate_on_submit():
            # Get user's id from database

            email = str(form.email.data)

            password = str(form.password.data)

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

@app.route("/emailVerification", methods=["GET", "POST"])
def emailVerification():
    """Email verification page"""

    return render_template("EmailVerification.html")
