import json
import logging
import aioredis
from aioredis.pubsub import Receiver
from aioredis.abc import AbcChannel
from config import read_config

config = read_config()
logger = logging.getLogger(__name__)
worker_queue = config["WORKER_QUEUE"]
websocket_channel = config["WEBSOCKET_CHANNEL"]


async def create_connection_pool(loop):
    logger.info("Initilizing redis connection pool started")
    pool = await aioredis.create_pool(
            (config["REDIS_HOST"], config["REDIS_PORT"]),
            minsize=5, maxsize=10,
            loop=loop)
    return pool


async def subscribe_to_channel(loop, redis_pool):
    mpsc = Receiver(loop=loop)

    logger.info("Aquiring redis connection from pool")
    connection = await redis_pool.acquire()

    logger.info("Subscribing to redis channel: {}".format(websocket_channel))
    await connection.execute_pubsub("subscribe", mpsc.channel(websocket_channel))
    return mpsc


async def subscription_reader(mpsc, handle_message):
    async for channel, msg in mpsc.iter():
        logger.debug("Subscription message")
        assert isinstance(channel, AbcChannel)
        handle_message(msg)
    logger.info("connection lost!")
