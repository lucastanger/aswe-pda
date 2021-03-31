#!/bin/bash
app="calendar-service"
docker build -t ${app} .
docker run -d --rm -p 5560:5560 \
  --name=${app} \
  ${app}
