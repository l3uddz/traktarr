FROM python:3.6-alpine3.7

ENV \
  # App directory
  APP_DIR=traktarr \
  # Branch to clone
  BRANCH=master \
  # Config file
  TRAKTARR_CONFIG=/config/config.json \
  # Log file
  TRAKTARR_LOGFILE=/config/traktarr.log

RUN \
  echo "** Upgrade all packages **" && \
  apk --no-cache -U upgrade && \
  echo "** Install OS dependencies **" && \
  apk --no-cache -U add git && \
  echo "** Get Traktarr **" && \
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
