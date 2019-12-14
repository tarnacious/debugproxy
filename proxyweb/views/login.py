from flask import render_template, Blueprint
from flask import request, url_for, flash, redirect
from flask import current_app
from flask_user import current_user
from proxyweb import app
from proxyweb.views import blueprint
from flask import Blueprint
from typing import Any
from config import read_config
from database.models import ProxySession
from sqlalchemy.exc import IntegrityError
from flask_user.email_manager import EmailManager
import database as db
import requests
from email.utils import parseaddr
from datetime import datetime
from flask_login import logout_user, login_user

import os
from proxyweb.views.forms import RegisterForm
from database.models import Organization, User

config = read_config()

blueprint = Blueprint('login', __name__, url_prefix='/account/')
url = config["WEBSITE_URL"]


@blueprint.route('register', methods=['GET', 'POST'])
def register() -> Any:
    show_captcha = current_app.config.get("USE_GOOGLE_CAPTCHA", False) == True
    site_key = current_app.config.get("GOOGLE_CAPTCHA_PUBLIC", '')
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():

        errors = False

        if show_captcha:
            try:
                recapture_response = request.form["g-recaptcha-response"]
                response = requests.post('https://www.google.com/recaptcha/api/siteverify', data =
                    {
                        'secret': current_app.config.get("GOOGLE_CAPTCHA_SECRET", ''),
                        'response': recapture_response
                    }
                )
                captcha_success = response.json()["success"]
            except:
                captcha_success = False

            if not captcha_success:
                errors = True
                form.captcha.errors.append('The capture did not validate, are you human?')

        valid_email_address = '@' in parseaddr(form.email.data)[1]

        if valid_email_address:
            user = User.query. \
                filter(User.email == form.email.data).first()
            if user:
                form.email.errors.append('User with the email already exists.')
                errors = True
        else:
            form.email.errors.append('Email is not valid.')
            errors = True

        if errors:
            return render_template('login/register.html', form=form, show_captcha=show_captcha, site_key=site_key)

        organization = Organization.query.filter(Organization.name == "debugproxy").first()

        if not organization:
            flash("Unable to create user. Please try again later.")
            return render_template('login/register.html', form=form, show_captcha=show_captcha, site_key=site_key)

        user = User()
        form.populate_obj(user)
        user.organization_id = organization.id
        user.active = True

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Unable to create user. Please try again later.")
            return render_template('login/register.html', form=form, show_captcha=show_captcha, site_key=site_key)

        email_manager = EmailManager(current_app)
        email_manager.send_registered_email(user, None, True)

        return redirect(url_for('login.registration_email_sent'))


    return render_template('login/register.html', form=form, show_captcha=show_captcha, site_key=site_key)


@blueprint.route('registration-email-sent', methods=['GET', 'POST'])
def registration_email_sent() -> Any:
    if not request.referrer or not request.referrer.endswith("register"):
        return redirect(url_for('home.home_page'))

    return render_template('login/registration_email_sent.html')


@blueprint.route('reset-password-email-sent', methods=['GET', 'POST'])
def reset_password_email_sent() -> Any:
    if not request.referrer or not request.referrer.endswith("forgot-password"):
        return redirect(url_for('home.home_page'))

    return render_template('login/reset_password_email_sent.html')


def send_reset_password_email(email):
    # Find user by email
    user_manager =  current_app.user_manager

    user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(email)
    if user:
        # Generate reset password link
        email_manager = EmailManager(current_app)

        # Send forgot password email
        email_manager.send_reset_password_email(user, None)

        # Store token
        # do we still need to do this?
        #if hasattr(user, 'reset_password_token'):
        #    db_adapter = user_manager.db_adapter
        #    db_adapter.update_object(user, reset_password_token=token)
        #    db_adapter.commit()

        # Send forgot_password signal
        # signals.user_forgot_password.send(current_app._get_current_object(), user=user)


@blueprint.route('forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Prompt for email and send reset password email."""
    user_manager =  current_app.user_manager

    # Initialize form
    from flask_user.forms import ForgotPasswordForm
    form = ForgotPasswordForm(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        email = form.email.data
        user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(email)

        if user:
            send_reset_password_email(email)

        # Prepare one-time system message
        flash("A reset password email has been sent", 'success')

        # Redirect to the resest password
        return redirect(url_for('login.reset_password_email_sent'))

    # Process GET or invalid POST
    return render_template("login/forgot_password.html", form=form)


@blueprint.route('reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ Verify the password reset token, Prompt for new password, and set the user's password."""
    # Verify token
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    if _call_or_get(current_user.is_authenticated):
        logout_user()

    is_valid, has_expired, user_id = user_manager.verify_token(
            token,
            user_manager.reset_password_expiration)

    if has_expired:
        flash('Your reset password token has expired.', 'error')
        return redirect(url_for('user.login'))

    if not is_valid:
        flash('Your reset password token is invalid.', 'error')
        return redirect(url_for('user.login'))

    user = user_manager.get_user_by_id(user_id)
    if user:
        # Avoid re-using old tokens
        if hasattr(user, 'reset_password_token'):
            verified = user.reset_password_token == token
        else:
            verified = True
    if not user or not verified:
        flash('Your reset password token is invalid.', 'error')
        return redirect(url_for('user.login'))

    # Mark email as confirmed
    user_email = emails.get_primary_user_email(user)
    user_email.confirmed_at = datetime.utcnow()

    # Initialize form
    form = user_manager.reset_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Invalidate the token by clearing the stored token
        if hasattr(user, 'reset_password_token'):
            db_adapter.update_object(user, reset_password_token='')

        # Change password
        hashed_password = user_manager.hash_password(form.new_password.data)
        user_auth = user.user_auth if db_adapter.UserAuthClass and hasattr(user, 'user_auth') else user
        db_adapter.update_object(user_auth, password=hashed_password)

        # We consider this to be confirmed
        user.set_active(True)
        db_adapter.commit()

        # Send 'password_changed' email
        if user_manager.enable_email and user_manager.send_password_changed_email:
            emails.send_password_changed_email(user)


        # Prepare one-time system message
        flash("Your password has been reset successfully.", 'success')

        # Auto-login after reset password or redirect to login page
        next = request.args.get('next', url_for("home.home_page"))
        return _do_login_user(user, next)                       # auto-login

    # Process GET or invalid POST
    return render_template("login/reset_password.html", form=form)


def _do_login_user(user: User, next: str, remember_me: bool=False) -> Any:
    # User must have been authenticated
    if not user:
        return unauthenticated()

    # Check if user account has been disabled
    if not _call_or_get(user.is_active):
        flash('Your account has not been enabled.', 'error')
        return redirect(url_for('user.login'))

    # Check if user has a confirmed email address
    user_manager = current_app.user_manager
    if user_manager.enable_email and user_manager.enable_confirm_email \
            and not current_app.user_manager.enable_login_without_confirm_email \
            and not user.has_confirmed_email():
        url = url_for('user.resend_confirm_email')
        flash('Your email address has not yet been confirmed.', 'error')
        return redirect(url_for('user.login'))

    # Use Flask-Login to sign in user
    login_user(user, remember=remember_me)

    return redirect(next)


def unauthenticated() -> Any:
    """ Prepare a Flash message and redirect to USER_UNAUTHENTICATED_ENDPOINT"""
    # Prepare Flash message
    url = request.url
    flash("You must be signed in to access this page", 'error')

    # quote the fully qualified url
    quoted_url = quote(url)

    # Redirect to USER_UNAUTHENTICATED_ENDPOINT
    user_manager = current_app.user_manager
    url =  url_for("home.home_page")
    return redirect(url + '?next=' + quoted_url)

def _call_or_get(function_or_property:Any) -> Any:
    if callable(function_or_property):
        return function_or_property()
    else:
        return function_or_property
