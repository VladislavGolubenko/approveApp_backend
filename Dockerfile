FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools
WORKDIR /approveApp


RUN set -eux \
    && apk update && apk upgrade  \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    build-base \
    python3-dev \
    bash \
    git \
    libffi-dev \
    openblas \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip \
    && rm -rf tmp

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./approveApp /approveApp

EXPOSE ${SERVER_PORT}
