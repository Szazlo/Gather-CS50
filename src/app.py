import sqlite3
from datetime import date
from datetime import timedelta
from functools import wraps
from pipes import Template
from urllib import response
from colorama import Fore, Style

from flask import (Flask, g, make_response, redirect, render_template, request,
                   session, url_for)
from flask_wtf import FlaskForm
from sqlalchemy import null
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session
from forms import *
from helpers import *

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


@app.route("/", methods=["GET",
                         "POST"])
def index():
    """Welcome page"""
    if request.method == "POST":
        # Redirect to dashboard if the user has just registered
        return redirect("/dashboard")

    if request.method == "GET":
        # Render dashboard if user is logged in

        print(f"{Fore.LIGHTBLUE_EX}Checking for session id{Style.RESET_ALL}")
        try:
            if session["email"]:
                print(
                    f"Session id found: {Fore.GREEN}{session['email']}{Style.RESET_ALL}")
                return redirect("/dashboard")
        except:
            print(f"{Fore.RED}No user logged in{Style.RESET_ALL}")
            return render_template("welcome.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard page"""
    # Get user's id from session
    user_id = session["email"]
    update = None

    try:
        update = session["update"]
        session.pop("update", None)
    except KeyError:
        update = None
        pass

    # Check if user  is verified
    verified = db.execute(
        "SELECT verified FROM users WHERE email = ?", (user_id,)).fetchone()
    if not verified:
        # The user is not verified and needs to verify their account to see the real dashboard
        return render_template("dashboard.html", username="unverified user")

    username = db.execute(
        "SELECT username FROM users WHERE email = ?", (user_id,)).fetchone()[0]

    # Failsafe for if the user is not in the database but the session is still active
    if username == None:
        return redirect("/logout")

    # Show meetings created by user
    db.row_factory = sqlite3.Row
    
    # TODO: Order by meeting_created_at and show most recent 8
    meetingsManagingSummary = db.execute(
        "SELECT * FROM meetings WHERE meeting_manager = ? LIMIT 8", (user_id,)).fetchall()
    meetingsManagingSummary = [dict(row) for row in meetingsManagingSummary]

    meetingsAttendingSummary = db.execute("SELECT * FROM meetings JOIN meeting_attendees ON meetings.meeting_id = meeting_attendees.meeting_id WHERE email = ? LIMIT 8",
                                          (session["email"],)).fetchall()
    
    # TODO: Make the summary above a dictionary

    try:
        if meetingsManagingSummary[0][0] is None or not meetingsManagingSummary:
            meetingsManagingSummary = None
    except:
        pass

    try:
        if meetingsAttendingSummary[0][0] is None or not meetingsAttendingSummary:
            meetingsAttendingSummary = None
    except:
        pass

    # Count meeting attendees
    # TODO
    """
    for meeting in meetingsManagingSummary:
        attendees = meeting[8].split(", ")
        if attendees is None:
            meeting.append(0)
        else:
            meeting.append(len(attendees))
    """

    return render_template("dashboard.html",
                           username=username,
                           greeting=timeBasedGreeting(),
                           meetingsManagingSummary=meetingsManagingSummary,
                           meetingsAttendingSummary=meetingsAttendingSummary,
                           update=update)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""

    form = registerForm()
    if request.method == "POST" and form.validate_on_submit():

        validator = registerValidator(form)
        if validator[1] != True:
            return render_template("register.html", form=validator[0])

        firstName = str(form.firstName.data)
        lastName = str(form.lastName.data)
        username = str(form.username.data)
        email = str(form.email.data).lower()
        hashed_password = str(generate_password_hash(form.password.data))

        db.execute("INSERT INTO users (username, email, password, firstName, lastName) VALUES (?, ?, ?, ?, ?)",
                   (username,
                    email,
                    hashed_password,
                    firstName,
                    lastName))
        print("Committing changes to database")
        db.commit()

        session["email"] = email
        return redirect("/")

    else:
        return render_template("register.html",
                               form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    form = loginForm()

    if request.method == "POST" and form.validate_on_submit():

        email = str(form.email.data).lower()
        password = str(form.password.data)
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)).fetchall()

        if len(user) != 1:
            return render_template("login.html",
                                   form=form,
                                   error="User does not exist")

        if check_password_hash(user[0][2], password):

            session["email"] = email
            return redirect("/")

        else:
            return render_template("login.html",
                                   form=form,
                                   error="Incorrect password")

    else:
        return render_template("login.html", form=form)


@app.route("/passwordreset", methods=["GET", "POST"])
def passwordReset():
    """ DELETE THIS SHIT BEFORE DEPLOYING """
    form = passwordresetForm()

    users = db.execute("SELECT username FROM users").fetchall()
    form.user.choices = [(user[0], user[0]) for user in users]
    if request.method == "POST":

        if form.validate_on_submit():
            # Get user's id from database
            users = db.execute("SELECT username FROM users").fetchall()
            form.user.choices = [(user[0], user[0]) for user in users]

    if request.method == "GET":
        return render_template("passwordreset.html",
                               form=form)


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


@app.route("/createMeeting", methods=["GET",
                                      "POST"])
@login_required
def createMeeting():
    """Page to create meetings"""
    form = meetingForm()

    if request.method == "POST":
        print(form.data)
        if not form.validate():
            print("Form not validated")
            print(form.errors)
            return render_template("createMeeting.html",
                                   form=form)
        # Server side validation
        error_count = 0
        if len(form.meeting_name.data) > 50:
            error_count += 1
            form.meeting_name.errors.append(
                "Meeting name must be less than 50 characters")

        if len(form.meeting_description.data) > 250:
            error_count += 1
            form.meeting_description.errors.append(
                "Meeting description must be less than 250 characters long.")

        # If the "Other" option is selected, replace the "Other" text with the actual value
        if form.meeting_type.data == "Other" and form.meeting_typeOther.data:
            form.meeting_type.data = form.meeting_typeOther.data
        if form.meeting_type.data != "Other" and form.meeting_typeOther.data:
            form.meeting_typeOther.data = None
        if form.meeting_type.data == "Select Type":
            error_count += 1
            form.meeting_type.errors.append(
                "Please select a meeting type")

        # If the form date type is not valid, add an error
        if form.meeting_dateType.data not in ["Set by me", "Agreed on by everyone"]:
            error_count += 1
            form.meeting_dateType.errors.append(
                "Please select a valid date type")

        # if form.meeting_dateType == "Set by me":
        #     form.meeting_dateRangeStart.data = None
        #     form.meeting_dateRangeEnd.data = None
        #     form.meeting_selectionPeriod.data = None

        # else:
        #     if form.meeting_dateRangeStart.data < date.today():
        #         error_count += 1
        #         form.meeting_dateRangeStart.errors.append(
        #             "Start date must be in the future")

        #     if form.meeting_dateRangeEnd.data < form.meeting_dateRangeStart.data:
        #         error_count += 1
        #         form.meeting_dateRangeEnd.errors.append(
        #             "End date must be after start date")

        #     if form.meeting_dateRangeEnd.data - form.meeting_dateRangeStart.data > timedelta(days=30):
        #         error_count += 1
        #         form.meeting_dateRangeEnd.errors.append(
        #             "Selection dates must be less than 30 days")

        if form.meeting_setDate.data < date.today():
            error_count += 1
            form.meeting_setDate.errors.append(
                "Meeting date must be in the future")

        if form.meeting_public == True and form.meeting_password.data:
            form.meeting_password.data = None

        """In this situation, a meeting would have four options:
        1. Meeting is public and no password, i.e anyone can join (this can be on a lookup page)
        2. Meeting is public and has a password, i.e anyone who has the password can join
        3. Meeting is private and no password, i.e only people who have the link can join
        4. Meeting is private with password, i.e only people who have the link and password can join
        """
        if error_count > 0:
            return render_template("createMeeting.html",
                                   form=form)

        form.meeting_startTime.data = form.meeting_startTime.data.strftime(
            "%H:%M")

        # Database insertion
        db.execute("INSERT INTO meetings (meeting_name, meeting_description, meeting_manager, meeting_location, meeting_setDate, meeting_startTime, meeting_public, meeting_password, meeting_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (form.meeting_name.data,
                    form.meeting_description.data,
                    session["email"],
                    form.meeting_location.data,
                    form.meeting_setDate.data,
                    form.meeting_startTime.data,
                    form.meeting_public.data,
                    form.meeting_password.data,
                    form.meeting_type.data,))
        print("Inserted meeting into database")
        db.commit()
        session["update"] = "Meeting created"
        return redirect("/dashboard")

    else:
        print("You got here via GET")
        return render_template("createMeeting.html",
                               form=form)


""" The syntax for the following function is as follows:
    After '/meeting/<>' we use the int: to convert the input url after meeting to an int,
    which is stored into a variable called meeting_id."""


@app.route("/meetings/")
@login_required
def meetingsSearch():
    """Page to search for public meetings

    Not yet implemented
    """

    return apology("What are you doing here?", "Hello?")


@app.route("/meetings/<int:meeting_id>", methods=["GET",
                                                  "POST"])
@login_required
def displayMeeting(meeting_id):
    """Use the custom URL to find the meeting."""

    meeting = db.execute(
        "SELECT meeting_id, meeting_public, meeting_manager FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
    if not meeting:
        return apology("Meeting does not exist",
                       404)

    meeting = meeting[0]

    attendees = db.execute(
        "SELECT meeting_attendees FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchone()

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
        meeting = db.execute(
            "SELECT * FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
        print(meeting)
        return render_template("AdminMeeting.html",
                               meeting=meeting[0],
                               attendees=attendees)

    # Check if user is attending the meeting
    if attendees != None:
        for attendee in attendees:
            if attendee == session["email"]:
                meeting = db.execute(
                    "SELECT * FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
                return render_template("attendeeMeeting.html",
                                       meeting=meeting[0],
                                       attendees=attendees)

    # If above loop fails, check if the meeting is public
    if meeting[1] == True:
        return render_template("attendeeMeeting.html",
                               meeting_id=meeting_id,
                               attendees=attendees)
        """ PSEUDOCODE FOR MEETING AVAILABILITY IN CALENDAR FORMAT
         If the meeting is set by the manager on a specific day, do not show the availability section
         If the meeting is set by the manager on a range of days, show the availability section
            In this section:
                Get the meeting's start and end dates
                Look at the length of the meeting ends
                As the calendar only shows 30 days, add an equal number of days to both before the start date
                and after the end date so it matches the 30 day format.

                Create the 30 day calendar.
                For each day in the 30 day calendar:20220611_140956909898_2.jpg
                    If the day is in the range of the meeting's start and end dates:
                        Display the day as available (Probably add the status of the day as available)
                    Else:
                        Display the day as unavailable

                    My 2 ways of doing this are.
                    Let each day be a list of lists, with each day having 3 components:
                        1. The day of the month
                        2. The month
                        3. The status of the day (available, unavailable, etc.):
                            Options would be:
                                * Available
                                * Selected
                                * Unavailable (Because it is not in the range)

                                In the future, I want to add more options like:
                                * Definetely available
                                * Possibly available
                                * Definitely unavailable

                                For example, if I chose the day available to be the 17th of July, the day's list would be:
                                [17, 7, "Available"]

                    The calendar is a list of lists, with each list being a day, with each day having 3 basic characteristics.
                    The user's available days will be validated and added to the database of meeting_attendees
                    *** Note: Add columnn to the meeting_attendees.

                    The manipulation of availability calculation and display will be determined by the third characteristic
                    of the day's list.

                    Probably will use Python's calendar module to create the calendar, or whatever.

                    For the display, I will use some grid or flex, with Jinja using the {{ if something in list}} statements
                    nested inside a for loop. The for loop will iterate through the calendar, and the if statement will
                    determine how to display the day in the calendar.
        """
    else:
        return render_template("isPrivate.html",
                               meeting_id=meeting_id)


@app.route("/joinMeeting", methods=["GET",
                                    "POST"])
@login_required
def joinMeeting():
    """Page to join a meeting"""

    if request.method == "POST":

        password = str(request.form.get("password"))
        meeting_id = request.form.get("meeting_id")
        print(f"password is {password}")
        print(f"Meeting id requested is {meeting_id}")
        actual_meeting = db.execute(
            "SELECT meeting_id, meeting_password FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()[0]
        print(f"DB meeting id and password are {actual_meeting}")
        if not actual_meeting:
            return apology("Maybe it was deleted", "Meeting does not exist")

        print(f"DB meeting's password is {actual_meeting[1]}")
        if actual_meeting[1] != password:
            return render_template("askForPassword.html", error="Invalid password")

        # Add user to meeting
        attendees = db.execute("SELECT meeting_attendees FROM meetings WHERE meeting_id = ?",
                               (meeting_id,)).fetchall()[0]
        print(attendees)
        # If the meeting has no attendees, set the attendees to the user
        if not attendees[0]:
            print("No attendees")
            db.execute("UPDATE meetings SET meeting_attendees = ? WHERE meeting_id = ?",
                       (session["email"] + ',',
                        meeting_id,))
            db.execute("INSERT INTO meeting_attendees (meeting_id, email) VALUES (?, ?)",
                       (meeting_id, session["email"],))
            db.commit()
        else:
            attendees = attendees[0][0].split(",")
            print(f"Attendees are {attendees}")
            for attendee in attendees:
                if attendee == session["email"]:
                    return render_template("askForPassword.html",
                                           error="You are already attending this meeting")
            attendees.append(session["email"])
            attendees = ",".join(attendees)
            print(f"New attendees are {attendees}")
            print("adding user to meeting")
            db.execute(
                "UPDATE meetings SET meeting_attendees = ? WHERE meeting_id = ?", (attendees, meeting_id))
            print("Inserting user to meeting attendees database")
            db.execute("INSERT INTO meeting_attendees (meeting_id, email) VALUES (?, ?)",
                       (meeting_id, session["email"],))
            print("Inserted user into meeting attendees database")
            db.commit()

        return redirect("/meetings/" + meeting_id)

    else:
        # Render the meeting if user is already attending the meeting
        attendees = db.execute("SELECT meeting_attendees FROM meetings WHERE meeting_id = ?",
                               (request.args.get("meeting_id"),)).fetchall()[0]
        print(attendees)
        if not attendees[0]:
            return render_template("askForPassword.html",
                                   meeting_id=request.args.get("meeting_id"))
        attendees = attendees[0][0].split(",")
        print(f"Attendees are {attendees}")
        for attendee in attendees:
            if attendee == session["email"]:
                return redirect("/meetings/" + meeting_id)
        if not request.args.get("meeting_id"):
            return apology("This section is under construction", 404)

        # If the user is not attending the meeting, ask for the password
        return render_template("askForPassword.html",
                               meeting_id=request.args.get("meeting_id"))


@ app.route("/leaveMeeting", methods=["GET"])
@ login_required
def leaveMeeting():
    """Page to leave a meeting"""

    if request.method == "GET":
        if not request.args.get("meeting_id"):
            return apology("This section is under construction",
                           404)

        meeting_id = request.args.get("meeting_id")
        meeting = db.execute(
            "SELECT meeting_attendees FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
        managerCheck = db.execute(
            "SELECT meeting_manager FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()

        if managerCheck[0][0] == session["email"]:
            return apology("You cannot delete your own meeting",
                           "You are the meeting manager")

        if not meeting:
            return apology("You are not attending this meeting")

        if len(meeting) != 1:
            return apology("Something went wrong",
                           "Something went wrong")

        meeting = meeting[0][0].split(",")
        print(meeting)
        for attendee in meeting:
            if attendee == session["email"]:
                meeting.remove(attendee)
                meeting = ",".join(meeting)
                db.execute(
                    "UPDATE meetings SET meeting_attendees = ? WHERE meeting_id = ?", (meeting, meeting_id))
                db.execute("DELETE FROM meeting_attendees WHERE meeting_id = ? AND email = ?",
                           (meeting_id, session["email"]))
                db.commit()
                session["update"] = "You have left the meeting"
                return redirect("/")


@ app.route("/deleteMeeting/<int:meeting_id>", methods=["GET"])
@ login_required
def deleteMeeting(meeting_id):
    """Page to delete a meeting"""
    meeting = db.execute(
        "SELECT meeting_id, meeting_manager FROM meetings WHERE meeting_id = ?", (meeting_id,)).fetchall()
    if not meeting:
        return apology("Meeting does not exist",
                       404)

    meeting = meeting[0]
    if meeting[1] != session["email"]:
        return apology("You are not the meeting manager",
                       403)

    db.execute("DELETE FROM meetings WHERE meeting_id = ?", (meeting_id,))
    db.execute("DELETE FROM meeting_attendees WHERE meeting_id = ?",
               (meeting_id,))
    db.commit()
    session["update"] = "Meeting deleted"
    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)
