#!/bin/bash

docker compose down
docker build -f node.Dockerfile -t node .
docker compose up
