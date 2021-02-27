#!/bin/bash
docker run -d -p 5570:5570 --name weather-container --env-file ./weather-auth.env weather-service:1.0
