#!/bin/bash
app="news-service"
docker build -t ${app} .
docker run -d -p 5575:5575 \
  --name=${app} \
  -v $PWD:/app ${app}
