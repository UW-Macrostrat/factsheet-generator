#!/bin/bash

docker build -f node.Dockerfile -t node .
docker build -f master.Dockerfile -t master .
docker run -it --network host --name master -v "$(pwd)"/data:/data master
# docker exec node python3 test_server.py 8000