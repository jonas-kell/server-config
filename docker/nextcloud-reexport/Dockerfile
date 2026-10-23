FROM nextcloud:34.0.5-fpm

RUN apt-get update && apt-get install -y procps smbclient libsmbclient-dev && rm -rf /var/lib/apt/lists/*
RUN pecl install smbclient
RUN docker-php-ext-enable smbclient
