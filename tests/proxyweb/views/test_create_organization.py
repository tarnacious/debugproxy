from . import ViewTestCase
import pytest


@pytest.mark.usefixtures('db')
class CreateOrganizationTests(ViewTestCase):

    def test_create_organization(self):
        self.login('admin@debugproxy.de', 'password')

        response = self.app.get('organizations/organizations')
        assert 'Create Organization' in response.data.decode()
        assert 'my_crazy_organization' not in response.data.decode()

        response = self.app.get('organizations/organizations/create')
        assert 'Save' in response.data.decode()

        response = self.app.post('organizations/organizations/create', data=dict(
            name='my_crazy_organization'
        ), follow_redirects=True)
        assert 'my_crazy_organization' in response.data.decode()

        response = self.app.get('organizations/organizations')
        assert 'my_crazy_organization' in response.data.decode()
