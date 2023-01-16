import json
import logging
import os
import time
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)

# create kafka topic
INPUT_KAFKA_TOPIC = "input-topic"
BOOT_STRAP_SERVERS = os.environ.get("BOOT_STRAP_SERVERS")

# producer
producer = KafkaProducer(bootstrap_servers=BOOT_STRAP_SERVERS)


def produce(data):
    producer.send(INPUT_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
    time.sleep(1)
