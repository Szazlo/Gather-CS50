import os
import requests
from flask import redirect, render_template, request, session, g
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id")is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function