from flask_user import UserManager
from proxyweb.views.forms import MyRegisterForm
from proxyweb.views.users import user_profile_page
from proxyweb.views.forms import UserRegisterForm
from flask import current_app, request, url_for, flash, redirect, render_template
from flask_user import current_user
from flask_login import logout_user, login_user
from datetime import datetime
from typing import Any
from flask_user import signals
from flask_user.translation_utils import lazy_gettext as _  # map _() to lazy_gettext()
from wtforms import ValidationError


class CustomUserManager(UserManager):

  def customize(self, app):
    self.RegisterFormClass = MyRegisterForm

  def confirm_email_view(self, token: str) -> Any:
    """ Verify the password reset token, Prompt for new password, and set the
    user's password."""

    if current_user.is_authenticated:
        logout_user()


    data_items = self.token_manager.verify_token(
        token,
        self.USER_CONFIRM_EMAIL_EXPIRATION)

    user = None
    if data_items:
        user, user_email = self.db_manager.get_user_and_user_email_by_id(data_items[0])

    if not user or not user_email:
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(url_for('user.login'))

    if user.password != '':
        flash(_('Confirmation token has been used and password set.'), 'error')
        return redirect(url_for('user.login'))

    # Initialize form
    form = UserRegisterForm(request.form)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Hash password
        new_password = form.new_password.data
        password_hash = self.hash_password(new_password)



        # Update user.password
        user_email.password = password_hash

        # Set UserEmail.email_confirmed_at
        user_email.email_confirmed_at=datetime.utcnow()

        # Save user
        self.db_manager.save_user_and_user_email(user, user_email)
        self.db_manager.commit()

        # Send confirmed_email signal
        #signals.user_confirmed_email.send(current_app._get_current_object(), user=user)
        #signals.user_changed_password.send(current_app._get_current_object(), user=user)

        # Flash a system message
        flash(_('Your email has been confirmed.'), 'success')

        # Auto-login after confirm or redirect to login page
        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_CONFIRM_ENDPOINT)
        return self._do_login_user(user, safe_next_url)  # auto-login

    # Process GET or invalid POST
    return render_template('login/register_set_password.html', form=form)

  def password_validator(self, form, field):
    is_valid = len(field.data) >= 6
    if not is_valid:
        raise ValidationError('Password must have at least 6 characters')
    return True
