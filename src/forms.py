from pipes import Template
from urllib import response
from wsgiref.validate import validator
from flask import Flask, render_template, request
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import *
from wtforms.validators import *

class registerForm(FlaskForm):
    firstName = StringField("First Name", [validators.DataRequired()])
    lastName = StringField("Last Name", [validators.DataRequired()])
    username = StringField("Username", [validators.DataRequired()])
    email = EmailField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    confirmPassword = PasswordField(validators=[InputRequired(), Length(min=8)])
    # recaptcha = RecaptchaField() ==> Removed, server response error
    tandcbox = BooleanField(validators=[validators.DataRequired()])
    submit = SubmitField("Sign up")

class loginForm(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Log in")

class passwordresetForm(FlaskForm):
    user = SelectField(validators=[InputRequired()])
    newpassword = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField("Reset password")

class meetingForm(FlaskForm):
    meeting_name = StringField(validators=[InputRequired()])
    meeting_description = StringField()
    meeting_location = StringField()
    meeting_dateRangeStart = DateField(validators=[InputRequired()])
    meeting_dateRangeEnd = DateField(validators=[InputRequired()])
    meeting_selectionPeriod = NumberRange(min=1, max=24)
    meeting_types = ["Select Type", "Social Event", "Meeting", "Orgy", "Other"]
    meeting_type= SelectField(choices=(meeting_types), validators=[InputRequired()])
    # L-> Will be a dropdown.
    meeting_public = BooleanField()
    meeting_pin = StringField(validators=[InputRequired(), Length(min=6, max=8)])
    
    submit = SubmitField("Create")
