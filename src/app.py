from itertools import product
from pipes import Template
import re, smtplib
from urllib import response
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render
from flask import Flask, render_template, request, make_response, redirect, session, url_for, g
from flask_session import Session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt, date
from wtforms import DecimalField
from forms import *
from database import get_db, close_db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from helpers import apology, isRoleBasedEmail, create_activation_link

app = Flask(__name__)

db = sqlite3.connect('app.db', check_same_thread=False)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "( . Y . )__Xyz143Babs"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["APP_NAME"] = "Gather"

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

    # Check if user  is verified
    verified = db.execute("SELECT verified FROM users WHERE email = ?", (user_id,)).fetchone()
    if not verified:
        # The user is not verified and needs to verify their account to see the real dashboard
        return render_template("dashboard.html", username="unverified user")

    username = db.execute("SELECT username FROM users WHERE email = ?", (user_id,)).fetchone()[0]

    # Failsafe for if the user is not in the database but the session is still active
    if username == None:
        return redirect("/logout") 

    currentTime = dt.now()
    greeting = ""
    if currentTime.hour < 12:
        greeting = "Good morning"
    elif 12 <= currentTime.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    # Show meetings created by user
    meeting_summary = db.execute("SELECT * FROM meetings WHERE meeting_manager = ?", (user_id,)).fetchall()
    
    try:
        if meeting_summary[0][0] is None or not meeting_summary:
            meeting_summary = None
    except:
        pass
    # Count meeting attendees
    """
    for meeting in meeting_summary:
        attendees = meeting[8].split(", ")
        if attendees is None:
            meeting.append(0)
        else:
            meeting.append(len(attendees))
    """
        
    return render_template("dashboard.html", username=username, greeting=greeting, meetings=meeting_summary)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""

    form = registerForm()

    if request.method == "GET":
        return render_template("register.html", form=form)

    else:
 
        if form.validate_on_submit():

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

            email = db.execute("SELECT email FROM users WHERE email = ?", 
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
            
            hashed_password = str(generate_password_hash(password))

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

            email = str(form.email.data)

            password = str(form.password.data)

            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            print(user)

            # Check if user exists
            if len(user) == 1:

                if check_password_hash(user[0][2], password):

                    session["email"]= email

                    return redirect("/")
                else:
                    return render_template("login.html", form=form, error="Incorrect password")
            else:
                return render_template("login.html", form=form, error="User does not exist")

    if request.method == "GET":
        return render_template("login.html", form=form)

@app.route("/passwordreset", methods=["GET", "POST"])
def Login():
    form = passwordresetForm()
    if request.method == "POST":
        
        if form.validate_on_submit():
            # Get user's id from database

            email = str(form.email.data)

            password = str(form.password.data)

            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            print(user)

            # Check if user exists
            if len(user) == 1:

                if check_password_hash(user[0][2], password):

                    session["email"]= email

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

    session.pop("email", None)
    return redirect("/")

# @app.route("/emailVerification", methods=["GET", "POST"])
# def emailVerification():
#     """Email verification page"""
    # Get user's id from session
    # email = session["email"]
    # activationLink = create_activation_link(email)

    # sender = "gatherappproject@gmail.com"
    # receivers = [email]

    # link = "http://" + request.host + "/emailVerification?link=" + activationLink
    # message = """From: From Gather gatherappproject@gmail.com
    # To: To {}
    # Subject: Email Verification
    
    # Please click the link below to verify your email address.
    # {}""".format(email, link)
    # try:
    #     smtp0bj = smtplib.SMTP()
    #     smtp0bj.sendmail(sender, receivers, message)
    #     print("Sent email?")
    # except smtplib.SMTPException:
    #     print("Error: unable to send email")
    # return render_template("EmailVerification.html")

@app.route("/createMeeting", methods=["GET", "POST"])
@login_required
def meetingCreator():
    """Page to create meetings"""
    form = meetingForm()

    if request.method == "GET":
        return render_template("createMeeting.html", form=form)
 
    else:
        if form.validate_on_submit():
            # Server side validation

            error_count = 0
            if len(form.meeting_name.data) > 50:
                error_count += 1
                form.meeting_name.errors.append("Meeting name must be less than 50 characters")

            
            if len(form.meeting_description.data) > 250:
                error_count += 1
                form.meeting_description.errors.append("Meeting description must be less than 250 characters")

            if form.meeting_dateRangeStart.data < date.today():
                error_count += 1
                form.meeting_dateRangeStart.errors.append("Start date must be in the future")
            
            if form.meeting_dateRangeEnd.data < form.meeting_dateRangeStart.data:
                error_count += 1
                form.meeting_dateRangeEnd.errors.append("End date must be after start date")

            # If user made event public yet still requires a pin

            if form.meeting_public.data == True and form.meeting_pin.data:
                error_count += 1
                form.meeting_pin.errors.append("Cannot add PIN to a public event")

            if error_count > 0:
                return render_template("createMeeting.html", form=form)

            # Database insertion
            db.execute("INSERT INTO meetings (meeting_name, meeting_description, meeting_manager, meeting_location, meeting_dateRangeStart, meeting_dateRangeEnd, meeting_public, meeting_pin, meeting_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (form.meeting_name.data, form.meeting_description.data, session["email"], form.meeting_location.data, form.meeting_dateRangeStart.data,
                            form.meeting_dateRangeEnd.data, form.meeting_public.data, form.meeting_pin.data, form.meeting_type.data,))
            print("Inserted meeting into database")
            db.commit()

            return redirect("/")


""" The syntax for the following function is as follows:
    After '/meeting/<>' we use the int: to convert the input url after meeting to an int,
    which is stored into a variable called meeting_id."""

@app.route("/meetings/<int:meeting_id>", methods=["GET", "POST"])
@login_required
def displayMeeting(meeting_id):
    """Use the custom URL to find the meeting."""
    """PSEUDOCODE FOR THE FOLLOWING FUNCTION:
    1. Get the meeting_id from the url
    2. Get the meeting from the database
    3. Get the user from the database
    4. Check if the user is the meeting manager
    5. If the user is the meeting manager, display the meeting information.
    6. If the user is not the meeting manager, 
        look at if the meeting is public and ask for the PIN if it is.
    7. Check if it matches the meeting's pin
    8. If the pin matches, run the following code
            * Check if the user is already in the meeting
            * If the user is not in the meeting, prompt them to join the meeting. The website will remember who the user is based on sessions.
              *** Do we require sign up?"""
    
    meeting = db.execute("SELECT meeting_id, meeting_public, meeting_manager FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
    meeting = meeting[0]

    if not meeting:
        return apology("Meeting does not exist", 404)

    attendees = db.execute("SELECT meeting_attendees FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchone()

    try:
        if attendees[0][0] != None:
            # Parse the attendees string into a list of emails
            attendees = attendees[0].split(",")
        else:
            attendees = None
    except:
        attendees = None
    # Page for meeting manager
    if meeting[2] == session["email"]:
        meeting = db.execute("SELECT * FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
        print(meeting)
        return render_template("AdminMeeting.html", meeting=meeting[0], attendees=attendees)

    # Check if user is attending the meeting
    if attendees != None:
        for attendee in attendees:
            if attendee == session["email"]:
                meeting = db.execute("SELECT * FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
                return render_template("attendeeMeeting.html", meeting=meeting[0], attendees=attendees)

    # If above loop fails, check if the meeting is public
    if meeting[1] == True:
        return render_template("attendeeMeeting.html", meeting_id=meeting_id, attendees=attendees)
    else:
        return render_template("isPrivate.html", meeting_id=meeting_id)

    

@app.route("/joinMeeting", methods=["GET", "POST"])
@login_required
def pinCheck():
    """Page to join a meeting"""

    if request.method == "GET":
        if not request.args.get("meeting_id"):
            return apology("How did you get there wtf.", 404)
        return render_template("askForPin.html", meeting_id=request.args.get("meeting_id"))

    else:
        Pin = str(request.form.get("PIN"))
        meeting_id = request.form.get("meeting_id")
        print(Pin)
        print(meeting_id)
        actual_meeting = db.execute("SELECT meeting_id, meeting_pin FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()[0]
        print(actual_meeting)
        if not actual_meeting:
            return apology("Meeting does not exist", 404)

        print(actual_meeting[1])
        if actual_meeting[1] != Pin:
            return render_template("askForPin.html", error="Invalid PIN")
        
        # Add user to meeting
        attendees = db.execute("SELECT meeting_attendees FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
        # If the meeting has no attendees, set the attendees to the user
        if attendees[0][0] == None:
            db.execute("UPDATE meetings SET meeting_attendees = ? WHERE meeting_id = ?", (session["email"], meeting_id,))
            db.commit()        
        else:
            attendees = attendees[0][0].split(",")
            for attendee in attendees:
                if attendee == session["email"]:
                    return render_template("askForPin.html", error="You are already attending this meeting")
            attendees.append(session["email"])
            attendees = ",".join(attendees)
            print(attendees)
            print("adding user to meeting")
            db.execute("UPDATE meetings SET meeting_attendees = ? WHERE meeting_id = ?", (attendees, meeting_id))
            db.commit()

        return redirect("/meetings/" + meeting_id)
    
@app.route("/deleteMeeting", methods=["GET", "POST"])
@login_required
def deleteMeeting():
    return apology("Not implemented yet", 404)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="