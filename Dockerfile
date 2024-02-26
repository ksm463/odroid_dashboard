FROM ubuntu:20.04

ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /fastapi-uiux

COPY . .

RUN apt-get update && \
    apt-get install -y tmux python3 python3-pip vim git

RUN ln -s $(which python3) /usr/bin/python

RUN pip install fastapi[all] sqlmodel board loguru dash
RUN pip install dash dash-core-components dash-html-components plotly
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install Adafruit-Blinka gpiod
