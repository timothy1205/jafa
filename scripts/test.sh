#!/usr/bin/bash

IMAGE=$(docker buildx build -q .)
docker run --rm $IMAGE python -m unittest discover -s backend/tests/  -p "*_test.py"
docker image rm $IMAGE > /dev/null 2>&1