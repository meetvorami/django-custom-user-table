from kafka import KafkaProducer

from config.config import KafkaSettings
from utils.kafka_utils import json_serializer


class KafkaProd:
    def __init__(self) -> None:
        kafka_settings = KafkaSettings()
        self.producer = KafkaProducer(
            bootstrap_servers=[kafka_settings.bootstrap_servers],
            value_serializer=json_serializer,
            retries=kafka_settings.retries,
            retry_backoff_ms=kafka_settings.retry_backoff_ms,
        )
        self.topic = kafka_settings.topic

    def send_event(self, event):
        try:
            self.producer.send(self.topic, event)
        except Exception as e:
            print(f"error in the code is : {e}")
