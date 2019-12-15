from proxyweb import app
import unittest
from database.models import User, Organization

from proxyweb.startup.create_users import create_users
from proxyweb.startup.create_users import find_or_create_user, find_or_create_role


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        create_users()

        admin_role = find_or_create_role('admin', u'Admin')

        # It would be nicer and quicker if users were created here an not looked
        # up.
        self.user = User.query.all()[0]
        self.organization = Organization.query.all()[0]


        self.non_system_admin = find_or_create_user(u'Admin',
                                                    u'Example',
                                                    u'user@debugproxy.de',
                                                    'password',
                                                    self.organization,
                                                    [admin_role]
                                                    )

        self.app = app.test_client()

    def login(self, username, password):
        return self.app.post('/user/sign-in', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/user/sign-out', follow_redirects=True)
