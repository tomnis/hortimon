#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys

from pi_sht1x import SHT1x
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient


def parse_args():
    """
    Parses command line arguments.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environment", help="garden environment. used as a tag in influxdb.")
    ap.add_argument("-d", "--data-pin", type=int, help="gpio data pin number.")
    ap.add_argument("-c", "--clock-pin", type=int, help="gpio clock pin number.")
    args = vars(ap.parse_args())
    return args


def read_sensor(data_pin, clock_pin):
    """
    Reads sensor values and returns tuple of (temperature, humidity, dew_point)
    """
    with SHT1x(14, 4, gpio_mode=GPIO.BCM) as sensor:
        temperature = sensor.read_temperature()
        humidity = sensor.read_humidity(temperature)
        dew_point = sensor.calculate_dew_point(temperature, humidity)
        print(sensor)

    temperature = temperature * 9/5.0 + 32
    dew_point = dew_point * 9/5.0 + 32

    return (temperature, humidity, dew_point)



def write_values(temperature, humidity, dew_point, environment):
    """
    Writes the given values to influx.
    """

    # TODO accept host and possibly series as arguments
    client = InfluxDBClient('hortimon-mothership.local', 8086, 'root', 'root', 'garden')
    client.create_database('garden')
    json_body = [
        {
            "measurement": "garden",
            "tags": {
                "environment": environment
            },
            "fields": {
                "temperature": temperature,
                "humidity": humidity,
                "dew_point": dew_point,
            }
        }
    ]

    print("writing to influx, environment=" + environment)
    client.write_points(json_body)



def main():
    args = parse_args()
    data_pin = args.get("data_pin")
    clock_pin = args.get("clock_pin")
    (temperature, humidity, dew_point) = read_sensor(data_pin, clock_pin)

    environment = args.get("environment")
    write_values(temperature, humidity, dew_point, environment)


if __name__ == "__main__":
        main()

