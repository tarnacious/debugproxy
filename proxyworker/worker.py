import time
import json
import base64
import asyncio
from redis import Redis
import logging
from config import read_config
from redis.exceptions import ConnectionError
from time import sleep
from proxyworker.database import DatabaseSession


from proxyserver.redis import create_connection_pool, subscribe_to_channel, \
    save_proxy_stats, subscription_reader, increment_counter, get_counter, \
    clean_counters

logger = logging.getLogger(__name__)
logger.info("Starting worker")

config = read_config()
websocket_channel = config["WEBSOCKET_CHANNEL"]
worker_queue = config["WORKER_QUEUE"]

strict_redis = Redis(host='localhost', port=6379, db=0)
loop = asyncio.get_event_loop()
redis_pool = loop.run_until_complete(
    create_connection_pool(loop)
)


def send_websocket_message(message):
    strict_redis.publish(websocket_channel, json.dumps(message))


def send_proxy_message(address, message):
    strict_redis.publish(address, message)


# import the handlers after the loop, redis pool are setup and messaging
# functions are created
from proxyworker.handlers.request import handle_request
from proxyworker.handlers.connect import handle_connect
from proxyworker.handlers.response import handle_response
from proxyworker.handlers.connect_ended import handle_connect_ended
from proxyworker.handlers.resume import handle_resume


def handle_message(data, database_session):
    logger.debug("Recieve message: {}, {}".format(
        data["type"],
        data["flow"]["id"]))

    if data["type"] == "request":
        handle_request(data, database_session)
        return

    if data["type"] == "response":
        handle_response(data, database_session)
        return

    if data["type"] == "intercept":
        handle_response(data, database_session)
        return

    if data["type"] == "error":
        handle_response(data, database_session)
        return

    if data["type"] == "user_resume":
        handle_resume(data, database_session)
        return

    if data["type"] == "connect":
        handle_connect(data, database_session)
        return

    if data["type"] == "connect-ended":
        handle_connect_ended(data, database_session)
        return
    if data["type"] == "closing-channel":
        # handled in the main loop
        return

    logger.debug("Recieve unknown message type: {}, {}".format(data["type"],
                                                               data["flow"]["id"]));


def cleanup():
    try:
        redis_pool.close()
    except:
        logger.exception("Exception disconnecting redis pool")
        pass

    try:
        loop.close()
    except:
        logger.exception("Exception closing async loop")
        pass


def worker():
    try:
        while True:
            message = None
            try:
                server, message = strict_redis.brpop(worker_queue)
            except KeyboardInterrupt:
                raise
            except ConnectionError:
                logger.info("Connection error")
                sleep(2)
            except:
                logger.exception("Error popping message")
                message = None

            if message:
                database_session = DatabaseSession()
                try:
                    data = json.loads(message.decode("utf-8"))
                    handle_message(data, database_session)
                except:
                    logger.exception("Error handling message: {}".format(message))
                finally:
                    database_session.close()
                    pass
    except:
        logger.exception("Fatal exception in worker loop")
    cleanup()
    logger.info("Ending worker process")


if __name__ == "__main__":
    worker()
