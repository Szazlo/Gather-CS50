from email.policy import default
from pipes import Template
from urllib import response
from wsgiref.validate import validator
from flask import Flask, request
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import *
from wtforms.validators import *
from 

class registerForm(FlaskForm):
    firstName = StringField("First Name", 
                            [validators.DataRequired()])
    lastName = StringField("Last Name",
                           [validators.DataRequired()
                            ])
    username = StringField("Username",
                           [validators.DataRequired()])
    email = EmailField(validators=
                                [InputRequired(), 
                                 Email()])
    password = PasswordField(validators=
                                    [InputRequired(),
                                     Length(min=8)])
    confirmPassword = PasswordField(validators=
                                             [InputRequired(),
                                              Length(min=8)])
    # recaptcha = RecaptchaField() ==> Removed, server response error
    tandcbox = BooleanField(validators=[validators.DataRequired()])
    submit = SubmitField("Sign up")

class loginForm(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Log in")

class passwordresetForm(FlaskForm):
    user = SelectField('users', choices=[])
    newpassword = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField("Reset password")

def DefaultType():
    def validate(form, field):
        if field.data == "Select Type":
            raise ValidationError("Please select a type")
    return validate

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
    meeting_type= SelectField(choices=(meeting_types), validators=[InputRequired(), DefaultType()])
    # L-> Will be a dropdown.
    meeting_typeOther = StringField(validators=[Length(min=3, max=20)])
    meeting_public = BooleanField()
    meeting_password = StringField(validators=[Length(min=6, max=8)])
    
    submit = SubmitField("Create")
    
    def RangeDateValidation(form, field):
        if field.data < form.meeting_dateRangeStart.data:
            raise ValidationError("End date must be after start date")
        if field.data < form.meeting_startTime.data:
            raise ValidationError("End date must be after start time")
