from . import ViewTestCase


class HomeTests(ViewTestCase):

    def test_no_data_items(self):
        self.login('admin@debugproxy.de', 'password')
        response = self.app.get('/')
        assert '<div class="home">' in response.data.decode()
