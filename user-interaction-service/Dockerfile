FROM python:3.11

LABEL version="0.1"
LABEL description="docker container for user interaction service"

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /home/app/user-interaction-service
# RUN mkdir -p /home/app/auth_sdk_dist
COPY . /home/app/user-interaction-service
# ADD ../auth-sdk/dist/ /home/app/auth_sdk_dist
WORKDIR /home/app/user-interaction-service
RUN ls
ENV AUTH_SERVICE_URL http://user:8001/

RUN pip install -r requirements.txt
