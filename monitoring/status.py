import asyncio
import aioredis
from aioredis import Redis
from redis import StrictRedis
from config import read_config
config = read_config()

from monitoring import spark

from proxyserver.redis import create_connection_pool, subscribe_to_channel, \
    save_proxy_stats, subscription_reader, increment_counter, get_counter, \
    clean_counters

def print_stats():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _print_stats(loop)
    )
    loop.close()

async def _print_stats(loop):
    worker_queue = config["WORKER_QUEUE"]

    pool = await create_connection_pool(loop)

    redis = Redis(pool)
    worker_queue_length = await redis.llen(worker_queue)

    requests_5s = await get_counter(pool, "requests", 5)
    requests_60s = await get_counter(pool, "requests", 60)
    requests_1h = await get_counter(pool, "requests", 3600)

    connects_5s = await get_counter(pool, "connects", 5)
    connects_60s = await get_counter(pool, "connects", 60)
    connects_1h = await get_counter(pool, "connects", 3600)

    errors_5s = await get_counter(pool, "errors", 5)
    errors_60s = await get_counter(pool, "errors", 60)
    errors_1h = await get_counter(pool, "errors", 3600)

    intercepted_5s = await get_counter(pool, "intercepted", 5)
    intercepted_60s = await get_counter(pool, "intercepted", 60)
    intercepted_1h = await get_counter(pool, "intercepted", 3600)

    not_authorized_5s = await get_counter(pool, "not_authorized", 5)
    not_authorized_60s = await get_counter(pool, "not_authorized", 60)
    not_authorized_1h = await get_counter(pool, "not_authorized", 3600)

    authorized_5s = await get_counter(pool, "authorized", 5)
    authorized_60s = await get_counter(pool, "authorized", 60)
    authorized_1h = await get_counter(pool, "authorized", 3600)

    ratelimited_5s = await get_counter(pool, "ratelimited", 5)
    ratelimited_60s = await get_counter(pool, "ratelimited", 60)
    ratelimited_1h = await get_counter(pool, "ratelimited", 3600)

    responses = await get_counter(pool, "responses", 5)

    print()
    print("Worker queue length   : {}".format(worker_queue_length))
    print()
    print("Requests 5s           : {}".format(format_list(requests_5s)))
    print("Requests 60s          : {}".format(format_list(requests_60s)))
    print("Requests 1h           : {}".format(format_list(requests_1h)))
    print()
    print("HTTPS connects 5s     : {}".format(format_list(connects_5s)))
    print("HTTPS connects 60s    : {}".format(format_list(connects_60s)))
    print("HTTPS connects 1h     : {}".format(format_list(connects_1h)))
    print()
    print("Responses             : {}".format(format_list(responses)))
    print()
    print("HTTP errors 5s        : {}".format(format_list(errors_5s)))
    print("HTTP errors 60s       : {}".format(format_list(errors_60s)))
    print("HTTP errors 1h        : {}".format(format_list(errors_1h)))
    print()
    print("ratelimited 5s        : {}".format(format_list(ratelimited_5s)))
    print("ratelimited 60s       : {}".format(format_list(ratelimited_60s)))
    print("ratelimited 1h        : {}".format(format_list(ratelimited_1h)))
    print()
    print("authorized 5s         : {}".format(format_list(authorized_5s)))
    print("authorized 60s        : {}".format(format_list(authorized_60s)))
    print("authorized 1h         : {}".format(format_list(authorized_1h)))
    print()
    print("not_authorized 5s     : {}".format(format_list(not_authorized_5s)))
    print("not_authorized 60s    : {}".format(format_list(not_authorized_60s)))
    print("not_authorized 1h     : {}".format(format_list(not_authorized_1h)))
    print()
    print("intercepted 5s        : {}".format(format_list(intercepted_5s)))
    print("intercepted 60s       : {}".format(format_list(intercepted_60s)))
    print("intercepted 1h        : {}".format(format_list(intercepted_1h)))

    #print(spark.spark_string(requests))

    redis.close()
    pool.close()
    await pool.wait_closed()

def format_list(l):
    return ", ".join(list(map(str, l[:10]))) + " " + spark.spark_string(l)

if __name__ == "__main__":
    print_stats()
