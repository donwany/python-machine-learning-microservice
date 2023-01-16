import json
import logging
from flask import Flask, request
from kafka_producer.producer import produce
from auth_svc import access
from auth import validate

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)


@app.route("/api/v1.0/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@app.route("/api/v1.0/predict", methods=["POST"])
def predict():
    response, err = validate.token(request)
    if err:
        return err
    resp = json.loads(response)

    if resp['admin']:
        if request.method == "POST":
            payload = request.get_json(force=True)
            logger.info(f"Sending data to kafka topic ... {payload}")
            produce(payload)
            logger.info("Data sent to predictor successfully!")
        return "Payload Sent, Success!", 200
    else:
        return "Not Authorized", 401


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=1958)
