import tornado.websocket
import json
import re
from proxywebsocket.session import read_session
from itsdangerous import BadSignature
from typing import List, Set, Dict, Tuple, Text, Optional, Any
from proxywebsocket.connections import Connections
from config import read_config
import logging
logger = logging.getLogger(__name__)

config = read_config()
worker_queue = config["WORKER_QUEUE"]

async def send_worker_message(redis_pool, message):
    with await redis_pool as redis:
        ok = await redis.lpush(worker_queue, json.dumps(message))

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = Connections() # type: Connections
    redis_pool = None

    #CORS_ORIGINS = ['localhost']

    def check_origin(self, origin: str) -> bool:
        #parsed_origin = urlparse(origin)
        # parsed_origin.netloc.lower() gives localhost:3333
        #return parsed_origin.hostname in self.CORS_ORIGINS
        return True

    def get_id(self) -> str:
        # should really do some authentication
        uri = self.request.uri
        m = re.search('id=(\d+)', uri)
        if m and m.groups(0):
            return m.groups(0)[0]

    def on_message(self, message: str) -> None:
        logger.info("SOCKET_MESSAGE: %s" % message)
        data = json.loads(message)
        if data["type"] == "resume":
            logger.info("resume message %s" % data["id"])
            message = {
                "type": "user_resume",
                "flow": {
                    "id": data["id"]
                },
                "user_id": self.user_id,
                "session_id": self.session_id
            }

            self.loop.create_task(
                send_worker_message(self.redis_pool, message))


    def open(self) -> None:
        self.client_key = None
        cookie_value = self.get_cookie("session")
        session_id = self.get_id()
        if not session_id:
            logger.error("no session id");
            # can we signal the specific error to the client here?
            self.close()
            return

        try:
            session = read_session(cookie_value)
        except BadSignature:
            logger.error("bad signature");
            session = None

        if session and "user_id" in session:
            user_id = session["user_id"]
            self.client_key = "{}_{}".format(user_id, session_id)
            self.user_id = user_id
            self.session_id = session_id
            self.connections.add_connection(self.client_key, self)

            self.write_message(json.dumps({
                "type":"log",
                "message": "connected"
            }))
        else:
            # can we signal the specific error to the client here?
            self.close()

    def on_close(self) -> None:
        if self.client_key:
            self.connections.remove_connection(self.client_key, self)

    def on_error(self) -> None:
        if self.client_key:
            self.connections.remove_connection(self.client_key, self)

    @classmethod
    def broadcast(cls, id: str, data: Any) -> None:
        logger.debug("Send message to: %s" % id)
        message = json.dumps(data, ensure_ascii=False).encode("utf8", "surrogateescape")
        cls.connections.broadcast(id, message)
