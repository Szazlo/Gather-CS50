from pipes import Template
from urllib import response
from wsgiref.validate import validator
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class registrationform(FlaskForm):
    firstname = StringField("First Name:", validators=[InputRequired()])
    lastname = StringField("Surname:", validators=[InputRequired()])
    dateofbirth = DateField("Date of birth:", validators=[InputRequired()])
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class regdetailsform(FlaskForm):
    phonenumber = StringField("Phone:", validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male'), ('Female'), ('Other')])
    addressline1 = StringField("Address:", validators=[InputRequired()])
    addressline2 = StringField("Address line 2:", validators=[InputRequired()])
    city = StringField("City:", validators=[InputRequired()])
    country = StringField("Country:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class loginform(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Login")

class redeem(FlaskForm):
    redeemcode = StringField("Enter a code to redeem:", validators=[InputRequired()])
    submit = SubmitField("Redeem")

class creategift(FlaskForm):
    codename = StringField("Enter Code:", validators=[InputRequired()])
    codevalue = IntegerField("Value:", validators=[InputRequired()])
    numberuses = IntegerField("Uses:", validators=[InputRequired()])
    submit = SubmitField("Create")

class creatediscount(FlaskForm):
    codename = StringField("Enter Code:", validators=[InputRequired()])
    createcode = IntegerField("Value (in %):", validators=[InputRequired(), NumberRange(0, 100)])
    numberuses = IntegerField("Uses:", validators=[InputRequired()])
    submit = SubmitField("Create")

class addproductform(FlaskForm):
    productname = StringField("Product Name:", validators=[InputRequired()])
    origin = StringField("Origin:", validators=[InputRequired()])
    description = TextAreaField("Description:", validators=[InputRequired()])
    price = DecimalField("Price:", validators=[InputRequired()])
    availability = IntegerField("Availability:", validators=[InputRequired()])
    submit = SubmitField("Add Product")

class updateproductform(FlaskForm):
    productname = StringField("Product Name:", validators=[InputRequired()])
    price = DecimalField("Set Price:", validators=[InputRequired()])
    availability = IntegerField("Set Availability:", validators=[InputRequired()])
    submit = SubmitField("Update")

class removeproductform(FlaskForm):
    productname = StringField("Product Name:", validators=[InputRequired()])
    confirmname = StringField("Retype to confirm:", validators=[InputRequired(), EqualTo("productname")])
    confirmdeletion = BooleanField("Are you sure you want to delete this product?", validators=[InputRequired()])
    submit = SubmitField("Delete")

class removeuserform(FlaskForm):
    username = StringField("Username Name:", validators=[InputRequired()])
    confirmname = StringField("Retype to confirm:", validators=[InputRequired(), EqualTo("username")])
    confirmdeletion = BooleanField("Are you sure you want to remove this user, including all data and credits?", validators=[InputRequired()])
    submit = SubmitField("Remove")