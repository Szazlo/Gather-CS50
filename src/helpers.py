import os
import requests
from flask import redirect, render_template, request, session, g
from functools import wraps
from database import get_db

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
    # Check for any role based email registrations
    username = ""
    for letter in email:
        if letter == "@":
            break
        else:
            username += letter
    print(username)

    roles = open("antiRoleBasedVerification.csv", "r")
    for role in roles:
        if username in role:
            roles.close()
            return True


    