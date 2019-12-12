import sys
import tornado.httpserver
import tornado.ioloop
import mitmproxy
import asyncio
from datetime import datetime
from mitmproxy import master
from mitmproxy.options import Options  # noqa
from proxyserver.messenger import Messenger
from proxyserver.redis import create_connection_pool, subscribe_to_channel, \
    save_proxy_stats, subscription_reader, increment_counter, get_counter, \
    clean_counters
from proxyserver.message_handler import handle_message


from proxyserver.proxy import Proxy
from proxyserver.addons import default_addons
import json
from typing import Any
from config import read_config
import logging
logger = logging.getLogger(__name__)

from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

AsyncIOMainLoop().install()

class Master(master.Master):
    def __init__(self,
                 options: Any,
                 server: mitmproxy.proxy.server.ProxyServer) -> None:

        options.body_size_limit = str(4 * 1000000) # 4mb for now.
        super().__init__(options, server)

        config = read_config()
        self.proxy_server_port = config["PROXYSERVER_PORT"]
        self.proxy_server_channel = config["PROXYSERVER_CHANNEL"]
        self.addons.add(*default_addons())


    def clean(self) -> None:
        for id in list(self.proxy.intercepts.keys()):
            intercept = self.proxy.intercepts[id]
            seconds = intercept.seconds_since_update()

            if not intercept.user_id:
                if seconds > 10:
                    logger.info("Flagging intercept {} due to inactivity".format(id))
                    self.proxy.intercept_timeout(id)

            if seconds > 300:
                logger.info("Flagging intercept {} due to inactivity".format(id))
                self.proxy.intercept_timeout(id)

    def handle_message(self, message):
        handle_message(message, self.proxy)

    def post_stats(self):

        data = {
            "address": self.proxy_server_channel,
            "connections": len(self.proxy.connections),
            "intercepts": len(self.proxy.intercepts),
            "time": str(datetime.now())
        }

        self.loop.create_task(
            save_proxy_stats(self.redis,
                             data))

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        self.loop = loop

        iol = tornado.ioloop.IOLoop.instance()
        iol.add_callback(self.start)
        tornado.ioloop.PeriodicCallback(lambda: self.tick(timeout=0), 5).start()
        tornado.ioloop.PeriodicCallback(lambda: self.clean(), 5000).start()
        tornado.ioloop.PeriodicCallback(lambda: self.post_stats(), 10000).start()

        logger.debug("Listening for messages on: {}".format(self.proxy_server_channel))
        try:
            self.redis = loop.run_until_complete(
                create_connection_pool(loop))
        except:
            logger.exception("Unable to create connection pool, exiting.")
            self.shutdown()
            sys.exit(-1)
            return

        messenger = Messenger(self.proxy_server_channel, loop, self.redis)
        self.proxy = Proxy(messenger, self.redis, loop)

        loop.run_until_complete(
            self.proxy.subscribe_to_queue()
        )

        self.addons.add(self.proxy)

        asyncio.ensure_future(clean_counters(self.redis))
        try:
            logger.info("Starting proxy server")
            iol.start()
        except KeyboardInterrupt:
            self.shutdown()
