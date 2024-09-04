import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()


class JwtSettings:
    def __init__(self):
        self.SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
        self.ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        )
        self.REFRESH_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 1440)
        )


class RedisSettings:
    def __init__(self):
        self.REDIS_HOST = os.getenv("REDIS_HOST")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT"))
        self.REDIS_DEPRECATED = bool(strtobool(os.getenv("REDIS_DEPRECATED", "True")))
        self.REDIS_DB = int(os.getenv("REDIS_DB"))
        self.REFRESH_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 1440)
        )


class KafkaSettings:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        self.retries = int(os.getenv("KAFKA_RETRIES"))
        self.retry_backoff_ms = int(os.getenv("RETRY_BACKOFF_MS"))
        self.topic = os.getenv("KAFKA_TOPIC")
        self.auto_offset_reset = os.getenv("KAFKA_AUTO_OFFSET_RESET")
        self.kafka_consumer_group = os.getenv("KAFKA_CONSUMER_GROUP_ID")
