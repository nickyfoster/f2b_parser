#!/bin/bash

script_folder=$(dirname `readlink -f "$0"`)
name=$(basename $script_folder)

docker exec -it ${name}_$1_1 /bin/sh
