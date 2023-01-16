#!/bin/bash

docker build --tag worldbosskafka/email-svc:v1.0.8 . -f Dockerfile
docker push worldbosskafka/email-svc:v1.0.8