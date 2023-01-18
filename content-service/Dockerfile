FROM python:3.11

LABEL version="0.1"
LABEL description="docker container for content service"

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /home/app/content-service
COPY . /home/app/content-service
WORKDIR /home/app/content-service

RUN pip install -r requirements.txt
