#!/bin/bash
composer install
app="aswe-pda-frontend"
docker build -t ${app}:1.0 .
docker run --rm -p 8080:80 \
  --name=${app} \
  ${app}:1.0