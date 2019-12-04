#!/bin/bash

script_folder=$(dirname `readlink -f "$0"`)
name=$(basename $script_folder)

docker-compose -f docker-compose.yml -p $name kill


