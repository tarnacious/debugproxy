import json
import logging
from base64 import b64encode
from mitmproxy.tools.web.app import flow_to_json
from proxyserver.redis import send_worker_message
import aioredis
from config import read_config

config = read_config()
logger = logging.getLogger(__name__)

class Messenger():

    def __init__(self, proxy_address, loop, connection_pool) -> None:

        self.proxy_address = proxy_address
        self.loop = loop
        self.connection_pool = connection_pool


    def send_message(self, message_type, intercept, proxy):

        message = {
            "type": message_type,
            "flow": flow_to_json(intercept.flow),
            "proxy_address": self.proxy_address
        };

        # Hack for now to handle disconnect CONNECT events.
        if message_type == "connect-ended":
            message["flow"]["status"] = "disconnected"

        if intercept.user_id:
            message["user_id"] = intercept.user_id

        if intercept.session_id:
            message["session_id"] = intercept.session_id

        if intercept.flow.response:
            data = intercept.flow.response.raw_content
            if data is not None:
                encoded = b64encode(data).decode("utf-8")
                message["response"] = encoded
            else:
                message["response"] = ""

        if intercept.flow.request:
            data = intercept.flow.request.raw_content
            if data is not None:
                encoded = b64encode(data).decode("utf-8")
                message["request"] = encoded
            else:
                message["request"] = ""

        async def send_message_wrapper(redis_pool, message, proxy):
            sent = await send_worker_message(redis_pool, message)
            if not sent:
                logging.info("message error {}".format(message))
                proxy.worker_error(message)


        self.loop.create_task(
            send_message_wrapper(self.connection_pool, message, proxy))

