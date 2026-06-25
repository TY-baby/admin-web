#!/bin/bash
set -e

echo "=== Base Room deploy ==="

# stop and rebuild containers
docker-compose down
docker-compose up -d --build

# clean old images
docker image prune -f

echo "=== deploy done ==="
echo "frontend: http://server-ip"
echo "backend:  http://server-ip:3000"
