import logging
from config import read_config
from redis import StrictRedis
from rratelimit import Limiter

logger = logging.getLogger(__name__)
config = read_config()

r = StrictRedis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], db=0)

rate_limits = config["RATE_LIMITS"]

limiters = []
for rate_limit in rate_limits:
    limit, period = rate_limit
    limiter = Limiter(r,
                      action='request_{}_{}'.format(limit, period),
                      limit=limit,
                      period=period)
    limiters.append(limiter)

def check_ratelimit(key):
    limit = False
    for limiter in limiters:
        result = limiter.checked_insert(key)
        if not result:
            limit = True
    return not limit
