#!/bin/bash

docker build --tag worldbosskafka/gate-svc:v2 . -f Dockerfile
docker push worldbosskafka/gate-svc:v2