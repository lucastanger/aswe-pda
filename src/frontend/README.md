# awse-pda-frontend
> A website that offers a UI for the PDA.

![PHP Version][php-image]
![Node.js Version][node-image]
![Docker compose Version][dockercompose-image]
![Docker Version][docker-image]
![Composer Version][composer-image]
![NPM Version][npm-image]

## Development Setup
Choose one of the following setup methods to run the frontend:

- **Standalone:** Run `start.sh` to start the frontend alone

It is located in the project root. Be sure to make it executable with `chmod +x ./run.sh` beforehand.
You'll need Composer and Docker to run this script, as defined by the above versioning tags.
- **Integrated:** Run docker-compose in the project root to start frontend together with all other services

- **Custom:** Run `docker-compose up` in frontend folder to orchestrate frontend only with the 
   services defined in `docker-compose.yml`

The frontend will be available at `localhost:8080`.

If you'd like to do it manually, please follow steps 1. trough 3.:

### 1. Dependencies

![Composer Version][composer-image] needed

The projects dependencies are managed with composer. The composer.json file defines the used dependencies.
All needed dependency files are copied from `/vendor` to
`/src/resources/assets` in order for them to be available in the webserver container.

To automatically make all dependencies available on the webserver, run

```
composer install
```


### 2. Docker

![Docker Version][docker-image] needed

A Dockerfile and docker-compose is available for running the PostgreSQL database, Apache, SMTP and Websocket Server
in a docker container. In order to set this up, the following steps are needed:
1. Build the apache image
```
docker build -t event-booking-apache:2020 .
```

2. Run docker-compose
```
docker-compose up -d
```

### 3. Configuration

The configuration for the website can be found in `/src/config.ini.php`.

## PHPStorm

### Docker

#### Dockerfile

Run Dockerfile to create image for docker-compose.yml.

1. Create new "Dockerfile" configuration
2. Context folder: "."
3. Image tag: "aswe-pda-frontend:[version]"

#### Docker-compose

Run database and webserver.

1. Create new "Docker-compose" configuration
2. Compose file(s): "./docker-compose.yml;"

### Debugging

Debugging via xdebug, all required packages are installed in the Dockerfile.

Installation:
1. Create "PHP Remote Debug" configuration
2. Install [browser extension](https://www.jetbrains.com/help/phpstorm/2019.3/browser-debugging-extensions.html?utm_campaign=PS&utm_content=2019.3&utm_medium=link&utm_source=product)
3. Run new created debug configuration
4. Open installed browser extension and enable debug

<!-- Markdown link & img dfn's -->
[php-image]: https://img.shields.io/badge/php-7.4.3-brightgreen?style=flat-square&logo=php
[composer-image]: https://img.shields.io/badge/composer-1.9.3-brightgreen?style=flat-square&logo=composer
[bootstrap-image]: https://img.shields.io/badge/bootstrap-4.3.1-brightgreen?style=flat-square&logo=bootstrap
[docker-image]: https://img.shields.io/badge/docker-20.10+-brightgreen?style=flat-square&logo=docker
[dockercompose-image]: https://img.shields.io/badge/dockercompose-1.25.0+-brightgreen?style=flat-square&logo=docker
[node-image]: https://img.shields.io/badge/node-12.13.0+-brightgreen?style=flat-square&logo=node.js
[npm-image]: https://img.shields.io/badge/npm-~7.5.3-brightgreen?style=flat-square&logo=npm
