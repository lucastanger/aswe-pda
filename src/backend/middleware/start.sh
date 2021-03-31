#!/bin/bash
app="middleware"
docker build -t ${app} .
docker run -d --rm -p 5600:5600 \
  --name=${app} \
  ${app}
