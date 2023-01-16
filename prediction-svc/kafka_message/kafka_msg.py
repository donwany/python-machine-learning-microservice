import json
import os
import logging
import time
import uuid
from kafka import KafkaProducer, KafkaConsumer

logging.basicConfig(level=logging.INFO)

# create kafka topic
INPUT_KAFKA_TOPIC = "input-topic"
OUTPUT_KAFKA_TOPIC = "output-topic"
BOOT_STRAP_SERVERS = "kafka-local.model-microservice.svc.cluster.local:9092"

# consumer
consumer = KafkaConsumer(INPUT_KAFKA_TOPIC,
                         group_id="iris-prediction",
                         bootstrap_servers=[BOOT_STRAP_SERVERS],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         api_version=(2, 5, 0)
                         )
# producer
producer = KafkaProducer(bootstrap_servers=BOOT_STRAP_SERVERS, api_version=(2, 5, 0))


def consume():
    while True:
        for message in consumer:
            logging.info(f"Consuming message from topic: {INPUT_KAFKA_TOPIC}")
            consume_msg = json.loads(message.value.decode("utf-8"))
            return consume_msg


def produce(message):
    logging.info(f"Producing message to topic: {OUTPUT_KAFKA_TOPIC}")
    while True:
        producer.send(OUTPUT_KAFKA_TOPIC,
                      json.dumps(message).encode("utf-8"))
        logging.info(f"Sending prediction data ... :- {message}")
        time.sleep(1)
