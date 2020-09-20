#!/usr/bin/env bash
set -e


APP_NAME='Crawler Projudi '$1
TARGET='crawler-projudi'
VERSION=$2
FORCE=$3

DIRTY=`git diff --quiet || echo 'dirty'`

if [ $DIRTY ]
then
  echo ERROR: Existem arquivos nao comitados
  exit 1
fi

if [ $VERSION ]
then
  DOCKER_VERSION=$VERSION
else
  DOCKER_VERSION=$(grep -o '^[0-9]\.[0-9]\.[A-Za-z0-9]*' 'src/VERSION')
fi

if [[ $1 == "PROD" ]]; then
    echo "Gerando versao PROD"
     REGION=us-east-1
     CLUSTER=producao-oito
     TASK_COUNT=1
     GENERATE_RELEASE=false
     FAMILY=PROD-${TARGET}
     SERVICE_NAME=PROD-${TARGET}
else
 echo "Gerando versao HML"
    REGION=us-east-1
    CLUSTER=apps-cluster
    TASK_COUNT=1
    GENERATE_RELEASE=true
    FAMILY=${TARGET}
    SERVICE_NAME=${TARGET}

    ./release-docker.sh "${DOCKER_VERSION}" ${TARGET} "${APP_NAME}"

fi

echo "family: ${FAMILY} service: ${SERVICE_NAME}"

if [ ${GENERATE_RELEASE} = "true" ]; then
  #TODO mudar versão VERSION
  git commit --all -m "Versão ${TARGET}-${DOCKER_VERSION}"
  git tag -a ${TARGET}-${DOCKER_VERSION} -m "Versão ${TARGET}-${DOCKER_VERSION}"
  if [ ${DONT_PUSH} != "true" ]; then
      git push
     git push --tags
  fi
fi
