from datetime import datetime
from mitmproxy.flow import Flow

class Intercept(object):
    def __init__(self, flow: Flow, connection) -> None:
        self.flow = flow
        self.connection = connection
        self.updated_at = datetime.now()
        self.session_id = None
        self.user_id = None
        self.modified = False
        self.intercepted = False
        self.rejected = False

    def seconds_since_update(self) -> float:
        return (datetime.now() - self.updated_at).total_seconds()
