#!/bin/bash

port_num="1"
CONTAINER_NAME="test-odroid-dashboard"
IMAGE_NAME="odroid-dashboard"
TAG="0.1"

port_num="1"
dashboard_path=$(pwd)


docker run \
    -it \
    -p ${port_num}8000:8000 \
    -p ${port_num}8085:8085 \
	-p ${port_num}8888:8888 \
    --name ${CONTAINER_NAME} \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${dashboard_path}:/odroid_dashboard \
    -e DISPLAY=$DISPLAY \
    -w /odroid_dashboard \
    ${IMAGE_NAME}:${TAG}
