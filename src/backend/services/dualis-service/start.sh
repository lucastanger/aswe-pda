#!/bin/bash
app="dualis-service"
docker build -t ${app} .
docker run -d -p 5555:5555 \
  --name=${app} \
  -v $PWD:/app ${app}