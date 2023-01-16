### Near Real-Time Machine Learning Microservice Design

### Tools
  - MySQL
  - MongoDB
  - Kubernetes (Minikube)
  - Docker
  - Kafka
  - Helm
  - k9s
  - JWT

### Services
  - Authentication
  - Gateway
  - Prediction
  - Notification ** (Send email of prediction)

### Install Kafka
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install kafka-local bitnami/kafka \
--set persistence.enabled=false,zookeeper.persistence.enabled=false

kubectl run kafka-local-client \
    --restart='Never' \
    --image docker.io/bitnami/kafka:3.3.1-debian-11-r19 \
    --namespace model-microservice \
    --command \
    -- sleep infinity

kubectl exec --tty -i kafka-local-client --namespace model-microservice -- bash
```
### Schema Registry
```shell
helm repo add schema-repo https://charts.bitnami.com/bitnami

helm install schema-registry-release schema-repo/schema-registry \
--set externalKafka.brokers=PLAINTEXT://kafka-local.model-microservice.svc.cluster.local:9092 \
--set kafka.enabled=false \
--set kafka.zookeeper.enabled=false 

# schema.registry.url
schema-registry-release.model-microservice.svc.cluster.local:8081
```

### Build Docker Image
```shell
docker login
docker build --tag worldbosskafka/auth-svc:v1.0.8 . -f Dockerfile
docker push worldbosskafka/auth-svc:v1.0.8

docker build --tag worldbosskafka/gateway-svc:v1.0.8 . -f Dockerfile
docker push worldbosskafka/gateway-svc:v1.0.8

docker build --tag worldbosskafka/iris-model-micro:v1.0.0 . -f Dockerfile
docker push worldbosskafka/iris-model-micro:v1.0.0
```

### Login
```shell
curl -X POST 'http://127.0.0.1:5000/login' -u "theodondre@gmail.com:admin123"

# postman
curl \
    --location \
    --request POST 'http://127.0.0.1:5000/login' \
    --header 'Authorization: Basic dGhlb2RvbmRyZUBlbWFpbC5jb206YWRtaW4xMjM='

# output token
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
```
### Validate
```shell
curl -X POST 'http://127.0.0.1:5000/validate' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRoZW9kb25kcmVAZ21haWwuY29tIiwiZXhwIjoxNjcyMTE5MTE3LCJpYXQiOjE2NzIwMzI3MTcsImFkbWluIjp0cnVlfQ.zyOq2pifWPb-qRaDHyTiadv-QFqPBz2Cfwyv-mN8NSU'

# output
{"admin":true,"exp":1669159143,"iat":1669072743,"username":"theodondre@gmail.com"}
```

### Python Test
```python
import requests
import json

url = "http://127.0.0.1:1958/predict"

payload = json.dumps({
                      "sepal_length": 2.0,
                      "sepal_width": 1.4,
                      "petal_length": 0.6,
                      "petal_width": 1.9})
headers = {
    'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
### Curl Test
```shell
# setosa
curl --request POST 'http://127.0.0.1:1958/predict' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRoZW9kb25kcmVAZ21haWwuY29tIiwiZXhwIjoxNjcyMzcwNTk1LCJpYXQiOjE2NzIyODQxOTUsImFkbWluIjp0cnVlfQ.Y87iqIU-QQ7KdDHWjmrWjq6b7-QrxA68o4vfr-_ujUo' \
--header 'Content-Type: application/json' \
--data-raw '{'sepal_length': 5.2, 'sepal_width': 3.6, 'petal_length': 1.5, 'petal_width': 0.3}'

# virginica
curl --request POST 'http://127.0.0.1:1958/predict' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRoZW9kb25kcmVAZ21haWwuY29tIiwiZXhwIjoxNjcyMzcwNTk1LCJpYXQiOjE2NzIyODQxOTUsImFkbWluIjp0cnVlfQ.Y87iqIU-QQ7KdDHWjmrWjq6b7-QrxA68o4vfr-_ujUo' \
--header 'Content-Type: application/json' \
--data-raw '{"sepal_length": 0.5, 'sepal_width': 2.6, 'petal_length': 6.5, 'petal_width': 1.7}'

# virsicolor
curl --request POST 'http://127.0.0.1:1958/predict' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRoZW9kb25kcmVAZ21haWwuY29tIiwiZXhwIjoxNjcyMzcwNTk1LCJpYXQiOjE2NzIyODQxOTUsImFkbWluIjp0cnVlfQ.Y87iqIU-QQ7KdDHWjmrWjq6b7-QrxA68o4vfr-_ujUo' \
--header 'Content-Type: application/json' \
--data-raw '{'sepal_length': 20.5, 'sepal_width': 2.6, 'petal_length': 6.5, 'petal_width': 1.7}'

```

### A POST request to `http://127.0.0.1:1958/predict` with the following body
```shell
{
  "sepal_length": 2.0,
  "sepal_width": 1.4,
  "petal_length": 0.6,
  "petal_width": 1.9
}
# response
{
    'sepal_length': 2.0, 
    'sepal_width': 1.4, 
    'petal_length': 0.6, 
    'petal_width': 1.9, 
    'status': 200, 
    'model_id': 'afe4e043-4d09-4bf9-9fe8-a6d030441221', 
    'prediction': 'setosa', 
    'model_type': 'LogisticRegressionModel', 
    'created_at': '2022-12-29 00:07:11.830677', 
    'message': 'Success'
}
```


The `gateway service` is responsible for making the `API request` to the predict endpoint. The `prediction service` consumes messages from the gateway-service, the message produced to `input-topic` 
to make predictions. The output of the prediction is sent to the `output-topic`. The prediction service is
both a `producer` and a `consumer`. When done, any service can finally consume from `output-topic` to any 
downstream service such as `mongoDB`.

`Schema Registry` used to encode and decode messages using `JSON schemas`, each topic requires messages to
conform to a specific schema, any other structure will emit errors.

`Authentication services` ensures users are registered to use the service. All registered users is stored in `MySQL`.

`Kafka UI` can run on `http://127.0.0.1:8080` once installed.

### References
  - https://marcosschroh.github.io/python-schema-registry-client/
  - https://pyjwt.readthedocs.io/en/stable/
  - https://kafka-python.readthedocs.io/en/master/
  - https://minikube.sigs.k8s.io/docs/start/
  - https://helm.sh/docs/intro/quickstart/
  - https://kubernetes.io/docs/tutorials/kubernetes-basics/
  - https://www.docker.com/
  - https://k9scli.io/topics/install/
  - https://github.com/provectus/kafka-ui/tree/master/charts/kafka-ui
  - https://github.com/obsidiandynamics/kafdrop