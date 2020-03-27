#!/bin/bash

# Script needs to run as sudo for access to gpio
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

./write_dht_sensor_values.py -e "$1" -s 2302 -p "$2"
