#!/bin/bash

script_folder=$(dirname `readlink -f "$0"`)
name=$(basename $script_folder)

docker-compose -f docker-compose.yml -p $name kill
docker-compose -f docker-compose.yml -p $name rm -f
docker-compose -f docker-compose.yml -p $name pull
docker-compose -f docker-compose.yml -p $name up $1
