from . import ViewTestCase
import pytest


@pytest.mark.usefixtures('db')
class CreateOrganizationTests(ViewTestCase):

    def test_create_organization(self):
        self.login('admin@debugproxy.de', 'password')

        response = self.app.get('organizations/organization/1')
        assert 'admin@debugproxy.de' in response.data.decode()
        assert 'swifty@email.com' not in response.data.decode()

        response = self.app.get('users/organization/1/users/create')
        assert 'Create User' in response.data.decode()
        assert 'Save' in response.data.decode()

        response = self.app.post('users/organization/1/users/create', data=dict(
            first_name='swifty',
            last_name='mcgee',
            email='swifty@email.com'
        ), follow_redirects=True)
        assert 'swifty@email.com' in response.data.decode()

        response = self.app.get('organizations/organization/1')
        assert 'admin@debugproxy.de' in response.data.decode()
        assert 'swifty@email.com' in response.data.decode()
