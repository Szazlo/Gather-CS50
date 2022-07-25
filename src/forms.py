import sqlite3
from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from helpers import isRoleBasedEmail

# def usernameTaken(form, field):
#         db = sqlite3.connect('app.db', check_same_thread=False)
#         username = db.execute("SELECT username FROM users WHERE username = ?", (form.field.data,)).fetchall()
#         if len(username) > 0:
#             raise ValidationError("Username already taken")

# def RoleBasedEmail(form, field):
#     if isRoleBasedEmail(form.email.data):
#         raise ValidationError("Email is not allowed")
    
# def emailTaken(form, field):
#     db = sqlite3.connect('app.db', check_same_thread=False)
#     email = db.execute("SELECT email FROM users WHERE email = ?", (form.email.data,)).fetchall()
#     if len(email) > 0:
#         raise ValidationError("Email already taken")
class registerForm(FlaskForm):
    firstName = StringField("First Name", validators=[InputRequired()])
    lastName = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", [InputRequired()])
    email = EmailField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    confirmPassword = PasswordField(validators=[InputRequired(), Length(min=8)])
    # recaptcha = RecaptchaField() ==> Removed, server response error
    tandcbox = BooleanField(validators=[InputRequired()])
    submit = SubmitField("Sign up")
    
        
class loginForm(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Log in")

class passwordresetForm(FlaskForm):
    user = SelectField('users', choices=[])
    newpassword = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField("Reset password")

class meetingForm(FlaskForm):
    meeting_name = StringField(validators=[InputRequired()])
    meeting_description = StringField()
    meeting_location = StringField()
    meeting_setDate = DateField()
    meeting_startTime = TimeField()
    meeting_dateRangeStart = DateField()
    meeting_dateRangeEnd = DateField()
    meeting_selectionPeriod = NumberRange(min=1, max=24)
    meeting_types = ["Select Type", "Social Event", "Meeting", "Charity Event", "Other"]
    meeting_type= SelectField(choices=(meeting_types), validators=[InputRequired()])
    # L-> Will be a dropdown.
    meeting_typeOther = StringField(validators=[Length(min=3, max=20)])
    meeting_public = BooleanField()
    meeting_password = StringField(validators=[Length(min=6, max=8)])
    
    submit = SubmitField("Create")

def registerValidator(form, isValid=True):
    """
    Register Form Validator
    Checklist:
    1. Username is not taken
    2. Email is not taken
    3. Email is not Role Based, e.g. marketing@gmail.com
    4. Password is at least 8 characters long
    5. Password and Confirm Password match
    6. Password has lowercase, uppercase, number, and special character
    """
    
    db = sqlite3.connect('app.db', check_same_thread=False)
    if len(db.execute("SELECT username FROM users WHERE username = ?", (form.username.data,)).fetchall()) > 0:
        isValid = False
        print("Username taken")
        form.username.errors.append("Username already taken")
    
    if isRoleBasedEmail(form.email.data):
        isValid = False
        form.email.errors.append("Email is not allowed")
    
    if len(db.execute("SELECT email FROM users WHERE email = ?", (form.email.data,)).fetchall()) > 0:
        isValid = False
        form.email.errors.append("Email already taken")
    
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
        isValid = False
        
    if form.password.data != form.confirmPassword.data:
        form.confirmPassword.errors.append("Passwords do not match")
    
    db.close()
    return form, isValid
    