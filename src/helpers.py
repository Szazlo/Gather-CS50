import os
import requests
from flask import redirect, render_template, request, session, g
from functools import wraps
from database import get_db
import email
import sqlite3
import string, random
from datetime import datetime as dt

def login_required(f):
    """Requires user to be logged in.

    Use as @login_required or @login_required().

    Checks for session and if no session is found, redirects to login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session["email"]:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def isRoleBasedEmail(email):
    """Check for any role based email registrations

    Examples include admin, marketing, etc."""
    username = ""
    for letter in email:
        if letter == "@":
            break
        else:
            username += letter

    roles = open("antiRoleBasedVerification.csv", "r")
    for role in roles:
        if username in role:
            roles.close()
            return True

def create_activation_link(email):
    """Create an activation link for the user"""
    db = sqlite3.connect('app.db', check_same_thread=False)
    
    activation_code = ''.join(random.choice(string.ascii_letters) for i in range(15))

    if db.execute("SELECT activationLink FROM verificationLinks WHERE activationLink = ?", (activation_code,)).fetchall():
        create_activation_link(email)
    else:
        db.execute("INSERT INTO verificationLinks (email, activationLink) VALUES (?, ?)", (email, activation_code))
        db.commit()
        db.close()
        return activation_code

def apology(message, code=400):
    """Render message as an apology to user.
    * Parameter 1: message to display to user
    * Parameter 2: HTTP status code
    """
    return render_template("apology.html", description=message, code=code)

def timeBasedGreeting():
    currentTime = dt.now()
    if currentTime.hour < 12:
        return "Good morning"
    elif 12 <= currentTime.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"