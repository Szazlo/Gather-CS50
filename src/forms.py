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
    tandcbox = BooleanField("I have read and agree to the privacy policy and terms of service.", [validators.DataRequired()])
    submit = SubmitField("Sign up")

class loginForm(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Log in")