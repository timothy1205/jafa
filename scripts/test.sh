#!/usr/bin/bash

DCO="docker compose -f docker-compose.yml -f docker-compose.dev.yml"
$DCO build

# Backend
$DCO run --rm jafa-backend python -m unittest discover -s backend/tests/  -p "*_test.py"

# Frontend
$DCO run --env CI=true --rm --no-deps jafa-frontend yarn --cwd frontend test --passWithNoTests