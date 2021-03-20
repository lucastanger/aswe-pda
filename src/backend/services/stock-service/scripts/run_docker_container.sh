#!/bin/bash
docker run -d -p 5585:5585 --name stock-container --env-file ./.secrets/stock-service.env stock-service:1.0
