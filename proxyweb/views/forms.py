from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, SubmitField, PasswordField, HiddenField, \
    validators, ValidationError, SelectField, IntegerField
from typing import Any
from flask_user.forms import RegisterForm
from os import path

# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])


class UserForm(FlaskForm):
    email = StringField('Email Address', validators=[
        validators.Length(min=1, max=100),
        validators.Email("Email address must be valid")])
    first_name = StringField('First name', validators=[
        validators.Length(min=1, max=50),
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.Length(min=1, max=50),
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')


class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')


class OrganizationForm(FlaskForm):
    name = StringField('First name', validators=[
        validators.DataRequired('Name is required')])
    submit = SubmitField('Save')


class UserRegisterForm(FlaskForm):
    password_missmatch = 'New Password and Retype Password did not match'
    new_password = PasswordField('New Password', validators=[
        validators.DataRequired('New Password is required')])
    retype_password = PasswordField('Retype New Password', validators=[
        validators.EqualTo('new_password',
                           message=password_missmatch)])
    next = HiddenField()
    submit = SubmitField('Register')

    def validate(self) -> bool:
        # Use feature config to remove unused form fields
        user_manager = current_app.user_manager
        delattr(self, 'retype_password')
        # Add custom password validator if needed
        has_been_added = False
        for v in self.new_password.validators:
            if v == user_manager.password_validator:
                has_been_added = True
        if not has_been_added:
            self.new_password.validators.append(user_manager.password_validator)
        # Validate field-validators
        if not super(UserRegisterForm, self).validate():
            return False
        # All is well
        return True


class RegisterForm(FlaskForm):
    email = StringField('email')
    captcha = StringField('g-recaptcha-response')
    submit = SubmitField('Register')


class SessionForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Save')

class InterceptForm(FlaskForm):
    query = StringField('Query')
    submit = SubmitField('Save')
