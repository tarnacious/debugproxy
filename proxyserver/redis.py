import json
import logging
import aioredis
import time
import bisect
import asyncio
from aioredis.pubsub import Receiver
from aioredis.abc import AbcChannel
from aioredis import Redis
from config import read_config

config = read_config()
logger = logging.getLogger(__name__)
worker_queue = config["WORKER_QUEUE"]
server_channel = config["PROXYSERVER_CHANNEL"]


async def create_connection_pool(loop):
    logger.debug("Initilizing redis connection pool started")
    pool = await aioredis.create_pool(
            (config["REDIS_HOST"], config["REDIS_PORT"]),
            minsize=5, maxsize=10,
            loop=loop)
    return pool


async def subscribe_to_channel(loop, redis_pool):
    mpsc = Receiver(loop=loop)

    logger.info("Aquiring redis connection from poool")
    connection = await redis_pool.acquire()

    logger.info("Subscribing to redis channel: {}".format(server_channel))
    something = await connection.execute_pubsub("subscribe", mpsc.channel(server_channel))
    return mpsc


async def save_proxy_stats(redis_pool, stat_data):
    try:
        key = "stats:proxyserver:" + server_channel
        redis = Redis(redis_pool)
        value = json.dumps(stat_data)
        ok = await redis.set(key, value, pexpire=2000)
    except:
        logger.debug("Error saving stats {}".format(stat_data))
        pass


async def send_worker_message(redis_pool, message):
    try:
        with await redis_pool as redis:
            ok = await redis.execute('lpush', worker_queue, json.dumps(message))
        return True
    except Exception as e:
        logger.info("Error sending worker message", e)
        return False


PRECISION = [1, 5, 60, 300, 3600, 18000, 86400]

async def increment_counter(redis_pool, name, count=1, now=None):
   try:
       now = now or time.time()
       redis = Redis(redis_pool)
       pipe = redis.pipeline()
       for prec in PRECISION:
          pnow = int(now / prec) * prec
          hash = '%s:%s'%(prec, name)
          pipe.zadd('known:', 0, hash)
          pipe.hincrby('count:' + hash, pnow, count)
       await pipe.execute()
   except Exception as e:
       logger.info("Error saving stats", e)

from datetime import datetime
async def get_counter(redis_pool, name, precision, samples=30):
   with await redis_pool as redis:
       hash = '%s:%s'%(precision, name)
       data = await redis.hgetall('count:' + hash)
       results = []
       pnow = int(time.time() / precision) * precision
       for index in range(samples):
           key = str(pnow - (index * precision)).encode("utf-8")
           results.append(int(data.get(key, 0)))
       return results

SAMPLE_COUNT = 30
async def clean_counters(redis_pool):
   with await redis_pool as connection:
       redis = Redis(connection)
       pipe = redis.pipeline()
       while True:
          start = time.time()
          index = 0
          known_count = await redis.zcard('known:')
          while index < known_count:
             hash = await redis.zrange('known:', index, index)
             index += 1
             if not hash:
                   break
             hash = hash[0].decode("utf-8")
             prec = int(hash.partition(':')[0])

             hkey = 'count:' + hash
             cutoff = time.time() - SAMPLE_COUNT * prec
             sample_keys = await redis.hkeys(hkey)
             samples = list(map(int, sample_keys))
             samples.sort()
             remove = bisect.bisect_right(samples, cutoff)

             if remove:
                print(hkey, samples[:remove])
                await redis.hdel(hkey, *samples[:remove])
                if remove == len(samples):
                   try:
                      pipe.watch(hkey)
                      length = pipe.hlen(hkey)
                      if not length:
                         pipe.multi()
                         pipe.zrem('known:', hash)
                         await pipe.execute()
                         index -= 1
                      else:
                         pipe.unwatch()
                   except redis.exceptions.WatchError:
                      pass

          duration = min(int(time.time() - start) + 1, 60)
          await asyncio.sleep(max(60 - duration, 1))



async def subscription_reader(mpsc, master):
    async for channel, msg in mpsc.iter():
        logger.debug("Subscription message")
        assert isinstance(channel, AbcChannel)
        master.handle_message(msg)
    logger.info("connection lost!")
    await master.subscribe_to_queue()
