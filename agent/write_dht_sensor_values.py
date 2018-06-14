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

import Adafruit_DHT
from influxdb import InfluxDBClient


def parse_args():
    """
    Parses command line arguments.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environment", help="garden environment. used as a tag in influxdb.")
    ap.add_argument("-s", "--sensor", help="dht sensor model. should be one of {11, 22, 2302}.")
    ap.add_argument("-p", "--pin", help="gpio data pin number.")
    args = vars(ap.parse_args())
    return args


def read_sensor(sensor, pin):
    """
    Reads sensor values and returns tuple of (temperature, humidity)
    Exits if we are not able to sucessfully read the sensor.
    """
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        return (temperature, humidity)
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    sensor = args.get("sensor")



def write_values(temperature, humidity, environment):
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
            }
        }
    ]

    print("writing to influx, environment=" + environment)
    client.write_points(json_body)



def main():
    args = parse_args()
    sensor_args = { 
        '11': Adafruit_DHT.DHT11,
        '22': Adafruit_DHT.DHT22,
        '2302': Adafruit_DHT.AM2302 
    }
    sensor = sensor_args[args.get("sensor")]
    pin = args.get("pin")
    (temperature, humidity) = read_sensor(sensor, pin)

    environment = args.get("environment")
    write_values(temperature, humidity, environment)


if __name__ == "__main__":
        main()

