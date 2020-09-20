#!/usr/bin/env bash
set -e
VERSION=$1
TARGET=$2
APP_NAME=$3
DOCKER_IMAGE=endereço:porta/${TARGET}

## COPY RESOURCES
rm -rf target/docker
mkdir -p target/docker
cp -r src/ target/docker
cp -af docker/. target/docker/

## BUILD DOCKER
docker build --no-cache target/docker --build-arg APP_NAME="${APP_NAME}" --build-arg OITO_VERSAO="${VERSION}"  --build-arg OITO_APP="${TARGET}"-"${VERSION}" -t "${DOCKER_IMAGE}":latest
docker tag "${DOCKER_IMAGE}":latest "${DOCKER_IMAGE}":"${VERSION}"
docker push "${DOCKER_IMAGE}":latest
docker push "${DOCKER_IMAGE}":"${VERSION}"
