import json
import os
import sys
import logging
import uuid
from datetime import datetime
# from kafka_message.kafka_msg import produce, consume
from kafka import KafkaProducer, KafkaConsumer
from predictor import PythonPredictor

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

INPUT_KAFKA_TOPIC = "input-topic"
OUTPUT_KAFKA_TOPIC = "output-topic"
BOOT_STRAP_SERVERS = "kafka-local.model-microservice.svc.cluster.local:9092"

consumer = KafkaConsumer(INPUT_KAFKA_TOPIC,
                         group_id="iris-prediction",
                         bootstrap_servers=[BOOT_STRAP_SERVERS],
                         auto_offset_reset='earliest',
                         enable_auto_commit=False,
                         api_version=(2, 5, 0)
                         )

producer = KafkaProducer(bootstrap_servers=BOOT_STRAP_SERVERS,
                         api_version=(2, 5, 0))


def main():
    logger.info("Loading model ...")
    model = PythonPredictor()

    logger.info("consuming messages from kafka topic ...")
    # consumed_message = consume()
    while True:
        for message in consumer:
            logging.info(f"Consuming message from topic: {INPUT_KAFKA_TOPIC}")
            consumed_message = json.loads(message.value.decode("utf-8"))

            logger.info("making prediction on consumed message ...")
            prediction = model.predict(consumed_message)

            if prediction:
                response = dict(
                    sepal_length=float(consumed_message['sepal_length']),
                    sepal_width=float(consumed_message['sepal_width']),
                    petal_length=float(consumed_message['petal_length']),
                    petal_width=float(consumed_message['petal_width']),
                    status=int(200),
                    model_id=str(uuid.uuid4()),
                    prediction=str(prediction),
                    model_type="LogisticRegressionModel",
                    created_at=str(datetime.now()),
                    message="Success"
                )

                logger.info(f"sending prediction to output topic ...{response}")
                producer.send(OUTPUT_KAFKA_TOPIC, json.dumps(response).encode("utf-8"))
            else:
                logger.error("Model failed to make predictions!")

    # TODO: SEND RESPONSE TO MONGODB


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
