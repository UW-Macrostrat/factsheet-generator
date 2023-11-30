#!/bin/bash

docker compose down
docker build -f node.Dockerfile -t node .
docker build -f pgvector.Dockerfile -t pgvector .
docker compose up

# docker build -f node.Dockerfile -t node .
# docker run -d -p 8000:8000 --name node node
# docker exec node python3 test_server.py 8000