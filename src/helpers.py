import os
import requests
from flask import redirect, render_template, request, session, g
from functools import wraps
from database import get_db
import email
import sqlite3
import string, random

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session["email"]:
                return redirect("/login")
        except KeyError:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def isRoleBasedEmail(email):
    """Check for any role based email registrations"""
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
    """Render message as an apology to user."""
    return render_template("apology.html", description=message, code=code)
        