#!/bin/bash

docker build --tag worldbosskafka/iris-model-micro:v2 . -f Dockerfile
docker push worldbosskafka/iris-model-micro:v2