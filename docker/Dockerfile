FROM python:3.6-alpine3.7

# Default branch to master
ARG BRANCH=master

ENV \
  APP_DIR=traktarr \
  BRANCH=${BRANCH} \
  TRAKTARR_CONFIG=/config/config.json \
  TRAKTARR_LOGFILE=/config/traktarr.log

RUN \
  echo "** Upgrade all packages **" && \
  apk --no-cache -U upgrade && \
  echo "** Install OS dependencies **" && \
  apk --no-cache -U add git && \
  echo "** Get Traktarr branch: ${BRANCH} **" && \
  git clone --depth 1 --branch ${BRANCH} https://github.com/l3uddz/traktarr.git /${APP_DIR} && \
  echo "** Install PIP dependencies **" && \
  pip install --no-cache-dir --upgrade pip setuptools && \
  pip install --no-cache-dir --upgrade -r /${APP_DIR}/requirements.txt

# Change directory
WORKDIR /${APP_DIR}

# Config volume
VOLUME /config

# Entrypoint
ENTRYPOINT ["python", "traktarr.py"]
