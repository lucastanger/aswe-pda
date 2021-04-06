#!/bin/bash
# Install all requirements for the unittests
echo "Installing all requirements for all services..."

# Middleware
pip install -r ./src/backend/middleware/requirements.txt

# Services
services=("maps" "calendar" "dualis" "news" "spotify" "stock" "t2s-s2t" "weather")
for service in "${services[@]}";
do
  pip install -r ./src/backend/services/"${service}"-service/requirements.txt --disable-pip-version-check
done
