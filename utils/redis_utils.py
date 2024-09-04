import redis

from config.config import RedisSettings


class RedisClient:
    def __init__(self):
        redis_obj = RedisSettings()
        self._client = redis.Redis(
            host=redis_obj.REDIS_HOST,
            port=redis_obj.REDIS_PORT,
            db=redis_obj.REDIS_DB,
            decode_responses=redis_obj.REDIS_DEPRECATED,
        )
        self.duration = redis_obj.REFRESH_TOKEN_EXPIRE_MINUTES
    
    def set(self, key,value):
        self._client.set(key,value,ex=self.duration)
    
    def get(self,key):
        return self._client.get(key)
    
    def delete(self,key):
        self._client.delete(key)