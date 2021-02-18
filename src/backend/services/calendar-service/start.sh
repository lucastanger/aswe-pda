#!/bin/bash
app="calendar-service"
docker build -t ${app} .
docker run -d --rm -p 5565:5565 \
  --name=${app} \
  ${app}