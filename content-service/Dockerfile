FROM python:3.11

LABEL version="0.1"
LABEL description="docker container for content service"

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /home/app/content-service
COPY . /home/app/content-service
WORKDIR /home/app/content-service
ENV AUTH_SERVICE_URL http://user:8001/
ENV USER_INTERACTION_URL http://userinteraction:8002/contents/books/top-contents

RUN pip install -r requirements.txt
