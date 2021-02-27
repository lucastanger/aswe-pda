#!/bin/bash
# Prepare apache source folder for dependency installation
rm -rf src/resources/assets
mkdir src/resources/assets

# Install composer dependencies and run post install script
composer install

# Install npm dependencies and post install script
npm install

app="aswe-pda-frontend"
docker build -t ${app}:1.0 .
docker run --rm -p 8080:80 \
  --name=${app} \
  ${app}:1.0