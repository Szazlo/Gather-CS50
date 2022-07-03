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
    recaptcha = RecaptchaField()
    submit = SubmitField("Sign up")

class loginForm(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Log in")