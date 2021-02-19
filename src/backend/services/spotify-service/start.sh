#!/bin/bash
app="spotify-service"
docker build -t ${app} .
docker run -d -p 5565:5565 \
  --name=${app} \
  -v $PWD:/app ${app}