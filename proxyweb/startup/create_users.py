from datetime import datetime
from proxyweb import app
import database as db
from database.models import Organization, User, Role, ProxySession
from typing import List, Set, Dict, Tuple, Text, Optional, Any


def create_debugproxy_organization(name):
    organization = Organization.query.filter(Organization.name == name).first()
    if not organization:
        organization = Organization(name=name)
        db.session.add(organization)
        db.session.commit()


def create_admin_command(email, password) -> None:
    admin_role = find_or_create_role('admin', u'Admin')
    system_admin_role = find_or_create_role('system_admin', u'System Admin')

    # Create organization
    organization = find_or_create_organization("debugproxy")

    db.session.commit()

    # Add users
    find_or_create_user(u'Admin',
                        u'User',
                        email,
                        password,
                        organization,
                        [admin_role, system_admin_role]
                        )

    # Save to DB
    db.session.commit()


def create_session_command(organization, email, password, session_user, session_password) -> None:
    # Create organization
    organization = find_or_create_organization(organization)

    db.session.commit()

    # Add users
    firstname, lastname = email.split("@")
    user = find_or_create_user(firstname,
                        lastname,
                        email,
                        password,
                        organization,
                        []
                        )

    # Save to DB
    db.session.commit()


    session = ProxySession.query.filter(ProxySession.username == session_user). \
                                 filter(ProxySession.password == session_password). \
                                 first()

    if not session:
        session = ProxySession()
        session.username = session_user
        session.password = session_password
        session.user_id = user.id

        db.session.add(session)
        db.session.commit()



def create_users() -> None:
    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    system_admin_role = find_or_create_role('system_admin', u'System Admin')

    # Create organization
    organization = find_or_create_organization("debugproxy")

    db.session.commit()

    # Add users
    find_or_create_user(u'Admin',
                        u'Example',
                        u'admin@debugproxy.de',
                        'password',
                        organization,
                        [admin_role, system_admin_role]
                        )

    find_or_create_user(u'User',
                        u'Example',
                        u'user@debugproxy.de',
                        'password',
                        organization,
                        []
                        )
    # Save to DB
    db.session.commit()


def find_or_create_role(name: str, label: str) -> Role:
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name: str,
                        last_name: str,
                        email: str,
                        password: str,
                        organization: Organization,
                        roles: List[Role]=[]) -> User:
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=app.user_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.utcnow(),
                    organization_id=organization.id)
        for role in roles:
            user.roles.append(role)
        db.session.add(user)
    return user


def find_or_create_organization(name: str) -> Organization:
    organization = Organization.query.filter(Organization.name == name).first()
    if not organization:
        organization = Organization(name=name)
        db.session.add(organization)
    return organization


def create_user_command(organization: str,
                        first_name: str,
                        second_name: str,
                        email: str,
                        password: str,
                        is_admin: str,
                        is_site_admin: str) -> User:


    organization = find_or_create_organization(organization)
    roles = []

    user = User.query.filter(User.email == email).first()
    if user:
        print("User already exists")

    if is_admin == "y" or is_admin == "Y":
        admin_role = find_or_create_role('admin', u'Admin')
        roles.append(admin_role)

    if is_site_admin == "y" or is_site_admin == "Y":
        system_admin_role = find_or_create_role('system_admin', u'System Admin')
        admin_role = find_or_create_role('admin', u'Admin')
        roles.append(system_admin_role)

    find_or_create_user(first_name,
                        second_name,
                        email,
                        password,
                        organization,
                        []
                        )

    db.session.commit()
