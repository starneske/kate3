#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $KATE3_DOCKER_IMAGE_LOCAL

docker build -t $KATE3_DOCKER_IMAGE_LOCAL:$KATE3_IMAGE_VERSION . 
