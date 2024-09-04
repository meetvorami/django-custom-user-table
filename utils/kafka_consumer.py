import json
import threading
import time

from kafka import KafkaConsumer

from config.config import KafkaSettings


class kafkaConsumer(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        kafka_settings = KafkaSettings()
        self.consumer = KafkaConsumer(
            kafka_settings.topic,
            bootstrap_servers=kafka_settings.bootstrap_servers,
            auto_offset_reset=kafka_settings.auto_offset_reset,
            group_id=kafka_settings.kafka_consumer_group,
            enable_auto_commit=False,
        )
        self.retries = kafka_settings.retries

    def run(self):
        while True:
            for message in self.consumer:
                value = json.loads(message.value)
                success = False
                retries = self.retries
                while retries > 0 and not success:
                    try:
                        print("Printing from consumer: value = ", value)
                        time.sleep(2)
                        self.consumer.commit()
                        success = True

                    except Exception as e:
                        print(f"Error while processing the task is: {e}")
                        retries -= 1
                        time.sleep(2)

                if not success:
                    print(
                        f"Message {value} failed after retries. Consider sending to a dead-letter queue."
                    )
                    self.consumer.commit()


def start_consumer_in_background():
    consumer_thread = kafkaConsumer()
    consumer_thread.daemon = True
    consumer_thread.start()
