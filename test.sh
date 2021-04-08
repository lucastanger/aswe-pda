#!/bin/bash
# Run all unittests
echo "Running all unittests..."

# Check if all requirement should be installed
if [ "$1" = "i" ] || [ "$1" = "install" ]; then
  bash install.sh
fi

# Middleware
cd ./src/backend/middleware/ || exit
bash test.sh
cd ../../../
cp ./src/backend/middleware/.coverage ./.coverage.middleware

# Services
services=("maps" "calendar" "dualis" "news" "spotify" "stock" "t2s-s2t" "weather")
for service in "${services[@]}";
do
  cd ./src/backend/services/"${service}"-service/ || exit
  if [ ! -f test.sh ]; then
    echo "File 'test.sh' for service '${service}' not found."
    cd ../../../../
    continue
  fi
  bash test.sh
  cd ../../../../
  cp ./src/backend/services/"${service}"-service/.coverage ./.coverage."${service}"
done

# Combine all coverage reports and create the html report
echo "Combining reports..."
coverage combine
coverage html -d docs/coverage
echo "Reports successfully written to docs/coverage."
