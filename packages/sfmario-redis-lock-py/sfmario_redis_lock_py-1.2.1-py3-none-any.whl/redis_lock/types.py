from datetime import timedelta
from typing import Union

from redis import Redis

RedisClient = Redis
LockKey = Union[bytes, str]
TimeOutType = Union[int, timedelta]
