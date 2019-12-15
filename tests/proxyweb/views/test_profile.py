from . import ViewTestCase
import pytest

@pytest.mark.usefixtures('db')
@pytest.mark.usefixtures('app')
class CreateOrganizationTests(ViewTestCase):

    def test_change_name(self):
        self.login('user@debugproxy.de', 'password')

        response = self.app.get('users/user/profile')
        assert 'User' in response.data.decode()
        assert 'Example' in response.data.decode()

        response = self.app.post('users/user/profile', data=dict(
            first_name='swifty',
            last_name='mcgee',
        ), follow_redirects=True)
        assert 'swifty' in response.data.decode()

        response = self.app.get('users/user/profile')
        assert 'swifty' in response.data.decode()
        assert 'mcgee' in response.data.decode()

    def test_change_password(self):
        self.login('user@debugproxy.de', 'password')

        response = self.app.get('user/change-password')
        assert 'Change password' in response.data.decode()


        # empty old password
        response = self.app.post('user/change-password', data=dict(
            old_password='',
            new_password='password',
            retype_password='password'
        ), follow_redirects=True)

        # REVISIT: default updated flask-user doesn't give specific error messages
        # assert 'Old Password is required' in response.data.decode()
        assert 'There was an error changing your password.' in response.data.decode()

        # incorrect old password
        response = self.app.post('user/change-password', data=dict(
            old_password='incorrect',
            new_password='password',
            retype_password='password'
        ), follow_redirects=True)

        # REVISIT: default updated flask-user doesn't give specific error messages
        # assert 'Old Password is incorrect' in response.data.decode()
        assert 'There was an error changing your password.' in response.data.decode()

        # no new password
        response = self.app.post('user/change-password', data=dict(
            old_password='password',
            new_password='',
            retype_password=''
        ), follow_redirects=True)

        # REVISIT: default updated flask-user doesn't give specific error messages
        # assert 'New Password is required' in response.data.decode()
        assert 'There was an error changing your password.' in response.data.decode()

        # new passwords don't match
        response = self.app.post('user/change-password', data=dict(
            old_password='password',
            new_password='password',
            retype_password='password2'
        ), follow_redirects=True)

        # REVISIT: default updated flask-user doesn't give specific error messages
        # assert 'New Password and Retype Password did not match' in response.data.decode()
        assert 'There was an error changing your password.' in response.data.decode()

        # success!
        response = self.app.post('user/change-password', data=dict(
            old_password='password',
            new_password='password',
            retype_password='password'
        ), follow_redirects=True)
        assert 'Your password has been changed successfully.' in response.data.decode()

        self.logout()

        response = self.login('admin@debugproxy.de', 'password')
        assert 'You have signed in successfully.' in response.data.decode()
