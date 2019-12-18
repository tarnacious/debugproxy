import pytest
import os
import database as the_db
from proxyweb.startup.create_app import create_app

db_connection = 'postgresql://postgres:password@localhost/website-test'

the_app = create_app()

the_app.config.update(dict(
    TESTING=True,
    LOGIN_DISABLED=False,
    MAIL_SUPPRESS_SEND=True,
    SERVER_NAME='localhost.localdomain',
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_TEST_DATABASE_URI',
                                           db_connection),
    WTF_CSRF_ENABLED=False
))


the_app.app_context().push()


@pytest.fixture(scope='session')
def app():
    return the_app


@pytest.fixture(scope='function')
def db():
    """
    Initializes and returns a SQLAlchemy DB object
    """
    the_db.session.close()
    the_db.drop_all()
    the_db.create_all()
    return the_db
