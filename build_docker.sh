#!/bin/bash

IMAGE_NAME="odroid-dashboard"
TAG="0.1"

docker build --no-cache -t ${IMAGE_NAME}:${TAG} .