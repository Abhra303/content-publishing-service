FROM python:3.11

LABEL version="0.1"
LABEL description="docker container for user auth service"

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /home/app/user-service
COPY . /home/app/user-service
WORKDIR /home/app/user-service

RUN pip install -r requirements.txt
