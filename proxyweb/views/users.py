from flask import redirect, render_template, Blueprint
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_accepted
from proxyweb import app
import database as db
from proxyweb.views.forms import UserProfileForm, \
    UserForm, UserRegisterForm

from database.models import ProxySession, Request, Intercept
from database.models import Organization, User
from sqlalchemy.exc import IntegrityError
from flask import current_app
from flask_user import emails
from flask_login import logout_user, login_user
from datetime import datetime
from flask_user.translations import gettext as _
from urllib.parse import quote      # Python 3.x
from proxyweb.views import blueprint
from typing import Any

blueprint = Blueprint('users', __name__, url_prefix='/users/')


@blueprint.route('admin')
@roles_accepted('admin')
def admin_page() -> Any:
    users = User.query.all()
    return render_template('users/admin_page.html', users=users)


@blueprint.route('organization/<organization_id>/users/create',
                       methods=['GET', 'POST'])
@roles_accepted('system_admin')
def create_user(organization_id: str) -> Any:
    form = UserForm(request.form)
    organization = Organization.query. \
        filter(Organization.id == organization_id).first()

    if request.method == 'POST' and form.validate():
        user = User()
        user.organization_id = organization.id
        form.populate_obj(user)
        user.active = True

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append('This email is already in use')
            return render_template('users/users/new.html',
                                   form=form,
                                   organization=organization)
        except:
            db.session.rollback()
            flash('Error saving user')
            return render_template('users/users/new.html',
                                   form=form,
                                   organization=organization)

        return redirect(url_for('organizations.organization',
                                organization_id=organization.id))

    return render_template('users/users/new.html',
                           form=form,
                           organization=organization)


@blueprint.route('organizations/user/<user_id>', methods=['GET', 'POST'])
@roles_accepted('system_admin')
def user_detail(user_id: str) -> Any:
    user = User.query. \
        filter(User.id == user_id).first()
    organization = Organization.query. \
        filter(Organization.id == user.organization_id).first()
    return render_template('users/users/details.html',
                           user=user,
                           organization=organization)


@blueprint.route('organizations/user/<user_id>/invite_user',
                       methods=['POST'])
@roles_accepted('system_admin')
def invite_user(user_id: str) -> Any:
    user = User.query. \
        filter(User.id == user_id).first()
    user_manager = current_app.user_manager
    token = user_manager.generate_token(int(user_id))
    confirm_email_link = url_for('users.register',
                                 token=token,
                                 _external=True)
    user.reset_password_token = token
    db.session.commit()

    try:
        emails.send_registered_email(user, None, confirm_email_link)
        flash("Invitaton sent")
    except Exception as e:
        flash("Error sending emails", 'error')

    return redirect(url_for('users.user_detail',
                            user_id=user_id))



@blueprint.route('delete-account', methods=['POST'])
@login_required
def delete_account() -> Any:
    db.session.delete(current_user)
    db.session.commit()

    return redirect(url_for('home.home_page'))


@blueprint.route('user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page() -> Any:
    # Initialize form
    form = UserProfileForm(request.form)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home.home_page'))

    if request.method == 'GET':
        form = UserProfileForm(first_name=current_user.first_name,
                               last_name=current_user.last_name)
        return render_template('users/user_profile_page.html',
                            form=form)
    # Process GET or invalid POST
    return render_template('users/user_profile_page.html',
                           form=form)
