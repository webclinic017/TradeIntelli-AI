import json

import redis


class RedisService:

    _redis_client = None

    @staticmethod
    def get_redis_client():
        if not RedisService._redis_client:
            RedisService._redis_client = redis.Redis(host='redis', port=6379, db=0)
        return RedisService._redis_client

    @staticmethod
    def set_value(key_name, time, value):
        r = RedisService.get_redis_client()
        if value:
            r.setex(key_name, time, json.dumps(value))
        else:
            raise Exception("Value can't be null")

    @staticmethod
    def get(key_name):
        r = RedisService.get_redis_client()
        value = r.get(key_name)
        if value:
            # Ensure the value is decoded to a string if it's in bytes
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            return json.loads(value)  # Use json.loads for strings
        return None

