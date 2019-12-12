from typing import List, Set, Dict, Tuple, Text, Optional, Any
from database.models import ProxySession, Request, Intercept
from database import Session
import logging
logger = logging.getLogger(__name__)

class DatabaseSession():

    def __init__(self):
        self.session = Session()

    def get_session(self):
        if not self.session:
            self.session = Session()
        return self.session

    def close(self):
        if self.session:
            self.session.close()

    def get_session_and_user_id(self, username: str, password: str) -> Tuple[str, str]:
        """
        Returns a tuple of (session_id, user_id) or None.
        """
        proxy_session = self.get_session().query(ProxySession) \
            .filter_by(username=username) \
            .filter_by(password=password) \
            .filter_by(is_active=True) \
            .first()

        if proxy_session:
            return (proxy_session.id, proxy_session.user_id)


    def save_request(self,
                     session_id: str,
                     id: str,
                     proxyserver: str,
                     state: str) -> None:

        try:
            request = Request(key=id,
                              session_id=session_id,
                              state=state,
                              proxyserver=proxyserver)

            self.get_session().add(request)
            self.get_session().commit()
            return True
        except:
            logger.exception("Error saving requeset.")
            try:
                self.get_session().rollback()
            except:
                pass
            return False


    def update_request(self,
                       session_id: str,
                       id: str,
                       state: str) -> None:

        try:
            request_data = self.get_session().query(Request). \
                filter(Request.key == id). \
                filter(Request.session_id == session_id). \
                first()

            request_data.state = state
            self.get_session().commit()
            return True
        except:
            logger.exception("Error saving requeset.")
            try:
                self.get_session().rollback()
            except:
                pass
            return False


    def get_request(self, request_id: str) -> Tuple[Any, Any, Any]:
        request = self.get_session().query(Request) \
            .filter_by(key=request_id) \
            .filter(Request.state.isnot(None)) \
            .first()

        if request:
            return request


    def get_intercepts(self, session_id: str) -> List[Tuple[str, str, str]]:
        intercepts = self.get_session().query(Intercept) \
            .filter(Intercept.session_id == session_id) \
            .all()

        return intercepts
