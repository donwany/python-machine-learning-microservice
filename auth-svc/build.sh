#!/bin/bash

docker login
docker build --tag worldbosskafka/auth:v2 . -f Dockerfile
docker push worldbosskafka/auth:v2