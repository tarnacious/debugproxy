from . import ViewTestCase


class HomeTests(ViewTestCase):

    def test_logged_in_home(self):
        self.login('user@debugproxy.de', 'password')
        response = self.app.get('/')
        assert 'Start Session' in response.data.decode()
