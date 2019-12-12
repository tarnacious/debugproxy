import asyncio
import aioredis
from logging.config import fileConfig
import logging
from redis import StrictRedis
from config import read_config
from proxyserver.redis import create_connection_pool, get_counter

from database.models import ProxySession, Request, Intercept, User
import concurrent_log_handler

config = read_config()
fileConfig('config/logging.ini')

def print_stats():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _print_stats(loop)
    )
    loop.close()

async def _print_stats(loop):
    worker_queue = config["WORKER_QUEUE"]

    pool = await create_connection_pool(loop)

    with await pool as redis:
        worker_queue_length = await redis.llen(worker_queue)

    requests = await get_counter(pool, "requests", 60)
    connects = await get_counter(pool, "connects", 60)
    errors = await get_counter(pool, "errors", 60)
    intercepted = await get_counter(pool, "intercepted", 60)
    not_authorized = await get_counter(pool, "not_authorized", 60)
    authorized = await get_counter(pool, "authorized", 60)
    ratelimited = await get_counter(pool, "ratelimited", 60)
    responses = await get_counter(pool, "responses", 60)


    session_count = ProxySession.query \
        .count()

    request_count = Request.query \
        .count()

    active_user_count = User.query \
        .filter_by(active=True) \
        .count()

    not_active_user_count = User.query \
        .filter_by(active=False) \
        .count()

    #intercept_count = Intercept.query \
    #    .count()

    print("proxy_sessions.value", session_count)
    print("requests.value", request_count)
    print("active_users.value", active_user_count)
    print("not_active_users.value", not_active_user_count)
    #print("user_intercepts.value", intercept_count)

    def calc_rate(l):
        rate = sum(map(int, l[1:6])) / 5
        return '{0:.2f}'.format(rate)


    print("requests_5_minute.value " + calc_rate(requests))
    print("connects_5_minute.value " + calc_rate(connects))
    print("errors_5_minutes.value " + calc_rate(errors))
    print("intercepted_5_minute.value " + calc_rate(intercepted))
    print("not_authorized_5_minute.value " + calc_rate(not_authorized))
    print("authorized_5_minute.value " + calc_rate(authorized))
    print("ratelimited_5_minute.value " + calc_rate(ratelimited))
    print("responses_5_minute.value " + calc_rate(responses))
    print("worker_queue.value " + str(worker_queue_length))

    redis.close()
    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    print_stats()
