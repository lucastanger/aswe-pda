#!/bin/bash
docker run -d -p 5570:5570 --name weather-container --env-file ./.secrets/weather-service.env weather-service:1.0
