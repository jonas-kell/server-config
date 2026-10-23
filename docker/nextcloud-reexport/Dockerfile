FROM nextcloud:33.0.10-fpm

RUN apt-get update && apt-get install -y procps smbclient libsmbclient-dev && rm -rf /var/lib/apt/lists/*
RUN pecl install smbclient
RUN docker-php-ext-enable smbclient
