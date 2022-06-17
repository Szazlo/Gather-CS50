from pipes import Template
from urllib import response
from wsgiref.validate import validator
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class indexform(FlaskForm):
    email = StringField(validators=[InputRequired()])
    submit = SubmitField("Sign up")

class login(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Sign In")