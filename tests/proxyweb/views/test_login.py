from . import ViewTestCase


class LoginTests(ViewTestCase):

    def test_home_page_runders_public_landing_page(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'Network debugging from your browser' in response.data

    def test_sessions_page_redirects_to_login(self):
        response = self.app.get('/sessions/generate', follow_redirects=True)
        assert "You must be signed" in response.data.decode()

    def test_invalid_email(self):
        response = self.login('admin', 'default')
        assert 'Invalid Email' in response.data.decode()

    def test_email_does_not_exist(self):
        response = self.login('admin@test.de', 'default')
        assert 'Incorrect Email and/or Password' in response.data.decode()

    def test_incorrect_password(self):
        response = self.login('admin@debugproxy.de', 'defaultx')
        assert 'Incorrect Email and/or Password' in response.data.decode()

    def test_login_logout(self):
        response = self.login('admin@debugproxy.de', 'password')
        assert 'You have signed in successfully.' in response.data.decode()
