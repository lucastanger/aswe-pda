# Define base image
FROM php:7.4.3-apache

# Update
RUN apt-get update

# Enable rewrite
RUN a2enmod rewrite
RUN service apache2 restart

# Enable debugging
RUN pecl install xdebug-2.9.4 && docker-php-ext-enable xdebug
RUN echo 'xdebug.remote_port=9000' >> /usr/local/etc/php/conf.d/xdebug.ini
RUN echo 'xdebug.remote_enable=1' >> /usr/local/etc/php/conf.d/xdebug.ini
RUN echo 'xdebug.remote_connect_back=1' >> /usr/local/etc/php/conf.d/xdebug.ini

# Copy source code and optional additional configs
COPY /src /var/www/html

# Create upload directory
RUN mkdir /data
RUN chmod 777 /data