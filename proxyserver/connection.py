from datetime import datetime
from mitmproxy.flow import Flow

class Connection(object):
    def __init__(self, flow: Flow) -> None:
        self.flow = flow
        self.updated_at = datetime.now()
        self.session_id = None
        self.user_id = None
        self.requests = dict()

    def seconds_since_update(self) -> float:
        return (datetime.now() - self.updated_at).total_seconds()
