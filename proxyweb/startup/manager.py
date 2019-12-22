from proxyweb import manager
import database as db
from proxyweb.startup.create_users import find_or_create_organization, \
    find_or_create_user, create_user_command, create_admin_command, \
    create_session_command, create_debugproxy_organization

from proxyweb.startup.create_users import create_users
from database.models import Organization, User


@manager.command
def init_db(): # type: ignore
    db.create_all()
    create_debugproxy_organization("debugproxy")

@manager.command
def drop_db(): # type: ignore
    db.session.commit()
    db.drop_all()

@manager.command
def clear_db(): # type: ignore
    db.session.query(Organization).delete()
    db.session.query(User).delete()
    db.session.commit()

@manager.command
def create_admin(email, password):
    create_admin_command(email, password)

@manager.command
def create_session(organization, email, password, session_user, session_password):
    create_session_command(organization, email, password, session_user, session_password)

@manager.command
def seed_db(): # type: ignore
    create_users()

@manager.command
def create_user_interactive(): # type: ignore
    organization = input("organization: ")
    email = input("email: ")
    first_name = input("first name: ")
    second_name = input("second name: ")
    password = input("password: ")
    is_admin = input("is admin [yN]: ")
    is_site_admin  = input("is site  admin [yN]: ")
    create_user_command(organization,
                        first_name,
                        second_name,
                        email,
                        password,
                        is_admin,
                        is_site_admin)


@manager.command
def create_user(organization, email, password): # type: ignore
    first_name = ""
    second_name = ""
    is_admin = "n"
    is_site_admin  = "n"
    create_user_command(organization,
                        first_name,
                        second_name,
                        email,
                        password,
                        is_admin,
                        is_site_admin)
