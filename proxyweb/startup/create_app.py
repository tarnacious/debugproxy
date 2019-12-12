from flask import Flask
from flask import flash, redirect, url_for, request
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_user import UserManager, SQLAlchemyAdapter
from flask_wtf.csrf import CSRFProtect, CSRFError
from proxyweb import app, manager
from proxyweb.startup.init_logging import init_logging

from proxyweb.views.users import blueprint as users_blueprint
from proxyweb.views.home import blueprint as home_blueprint
from proxyweb.views.organizations import blueprint as organizations_blueprint
from proxyweb.views.sessions import blueprint as sessions_blueprint
from proxyweb.views.intercepts import blueprint as intercepts_blueprint
from proxyweb.views.requests import blueprint as requests_blueprint
from proxyweb.views.certificates import blueprint as certificates_blueprint
from proxyweb.views.login import blueprint as login_blueprint
from config import read_config
import concurrent_log_handler
import logging

def create_app() -> Flask:
    app.config.update(read_config())

    if app.testing:
        app.config['WTF_CSRF_ENABLED'] = False

    # Setup Flask-Mail
    Mail(app)

    # Setup WTForms CsrfProtect
    csrf = CSRFProtect(app)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField, Field

    def is_hidden_field_filter(field: Field) -> bool:
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup a logger
    # REVISIT: This line now seems to break the logging.
    # app.logger
    from logging.config import fileConfig
    fileConfig('config/logging.ini')

    app.logger.info("create_app")

    # Setup Flask-User to handle user account related forms
    from database.models import User, UserInvitation
    from proxyweb.views.forms import MyRegisterForm
    from proxyweb.views.users import user_profile_page
    from proxyweb.views.forms import password_validator

    import database
    db_adapter = SQLAlchemyAdapter(database, User, UserInvitationClass=UserInvitation)

    UserManager(db_adapter,
                app,
                register_form=MyRegisterForm,
                user_profile_view_function=user_profile_page,
                password_validator=password_validator
                )

    app.register_blueprint(home_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(organizations_blueprint)
    app.register_blueprint(sessions_blueprint)
    app.register_blueprint(intercepts_blueprint)
    app.register_blueprint(requests_blueprint)
    app.register_blueprint(certificates_blueprint)
    app.register_blueprint(login_blueprint)

    app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        flash.error("Session timed out", "error")
        return redirect(url_for('user.login'))

    return app
