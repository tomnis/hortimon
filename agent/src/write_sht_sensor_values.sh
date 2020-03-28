#!/bin/bash

#
# Usage: write_sdh_sensors.sh <tag> <data pin> <clock pin>
#

# Script needs to run as sudo for access to gpio
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

python3 ./write_sht_sensor_values.py -e "$1" -d "$2" -c "$3"
