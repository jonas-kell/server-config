# How to push images that re-export the nextcloud docker image with additional features

## How to find the correct arch

```cmd
uname -m
```

For a raspberry pi 4 this is aarch64

## Why?

Seems to be the correct method of including smb support for the nextcloud installation.

<!-- image: needed for php-smbclient support https://github.com/nextcloud/helm/issues/205#issuecomment-2252118329 -->

Was used by default: docker.io/library/nextcloud:32.0.3-apache
When nginx + fpm: docker.io/library/nextcloud:32.0.3-fpm

## How to push the image

Make sure to update the tag if required

```cmd
docker buildx create --use
docker buildx inspect --bootstrap

docker login

cd docker/nextcloud-reexport

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t kellehorreur/nextcloud:32.0.3-fpm \
  --push .
```
