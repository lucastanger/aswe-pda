#!/bin/bash
app="maps-service"
docker build -t ${app} .
docker run -d --rm -p 5580:5580 \
  --name=${app} \
  ${app}