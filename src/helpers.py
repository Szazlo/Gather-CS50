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

    


    