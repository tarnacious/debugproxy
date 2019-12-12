import sys
import random
import threading
import time
import json
from time import sleep

import logging
logger = logging.getLogger(__name__)


from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

AsyncIOMainLoop().install()

from proxywebsocket.redis import create_connection_pool, subscribe_to_channel, \
    subscription_reader
import tornado
from tornado import web
from proxywebsocket.websocket import WebSocketHandler
from config import read_config
config = read_config()

def get_id(data):
    return "{}_{}".format(data["user_id"],
                          data["session_id"])

def handle_message(message):
    try:
        data = json.loads(message.decode("utf-8"))
        if data["type"] == "closing-channel":
            logger.info("close channel signal")
            return
        session = get_id(data)
        logger.debug("Message {} {}".format(session, data["flow"]["id"]))
        WebSocketHandler.broadcast(session, data["flow"])
    except Exception as e:
        logger.exception("Exceptions handling message")

async def subscribe(loop, redis):
    keep_looping = True
    while keep_looping:
        try:
            subscriber = await subscribe_to_channel(loop, redis)
            await subscription_reader(subscriber, handle_message)
            logger.error("Subscription readed finished?")
        except Exception as e:
            logger.error("Error subscribing to redis channel, sleeping for a bit", e)
            await asyncio.sleep(5)

def main():
    application = web.Application([(r"/updates", WebSocketHandler)])
    iol = tornado.ioloop.IOLoop.instance()
    loop = asyncio.get_event_loop()

    try:
        redis = loop.run_until_complete(
            create_connection_pool(loop))
    except:
        logger.exception("Unable to connect to redis on startup. ")
        sleep(5)
        logger.info("Shutting down.")
        sys.exit(-1)


    WebSocketHandler.redis_pool = redis
    WebSocketHandler.loop = loop

    application.listen(8081)
    try:
        loop.run_until_complete(
            subscribe(loop, redis))
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt")


if __name__ == "__main__":
    main()

