import pytest
import unittest
from proxyweb import db
from proxyweb.models.models import Organization, User, ProxySession


@pytest.mark.usefixtures('db')
class TestDataItem(unittest.TestCase):

    def setUp(self):
        self.organization = Organization(name="test_org")
        db.session.add(self.organization)
        db.session.commit()

        self.user = User(email=u"test@email.com")
        self.user.organization_id  = self.organization.id
        db.session.add(self.user)
        db.session.commit()

    def test_adding_and_querying_simple(self):
        proxy_session = ProxySession(user_id=self.user.id,
                                     username="myuser",
                                     password="mypass")

        db.session.add(proxy_session)
        db.session.commit()

        found_proxy_sessions = ProxySession.query.all()
        assert len(found_proxy_sessions) == 1
