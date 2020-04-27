#!/usr/bin/python3

import argparse
import time

from pi_sht1x import SHT1x
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
import schedule


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
    with SHT1x(data_pin, clock_pin, gpio_mode=GPIO.BCM) as sensor:
        temperature = sensor.read_temperature()
        humidity = sensor.read_humidity(temperature)
        dew_point = sensor.calculate_dew_point(temperature, humidity)
        # print(sensor)

    temperature = temperature * 9/5.0 + 32
    dew_point = dew_point * 9/5.0 + 32

    return (temperature, humidity, dew_point)



def write_values(temperature, humidity, dew_point, environment):
    """
    Writes the given values to influx.
    """

    # TODO accept host and possibly series as arguments
    client = InfluxDBClient(host='isengard.lan', port=80, path='/influxdb',  username='root', password='root', database='garden')
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

    # print("writing to influx, environment=" + environment)
    client.write_points(json_body)


def sample(data_pin, clock_pin, environment):
    (temperature, humidity, dew_point) = read_sensor(data_pin, clock_pin)
    write_values(temperature, humidity, dew_point, environment)



def main():
    args = parse_args()
    data_pin = args.get("data_pin")
    clock_pin = args.get("clock_pin")
    environment = args.get("environment")

    schedule.every(30).seconds.do(lambda: sample(data_pin, clock_pin, environment))

    while True:
        schedule.run_pending()
        time.sleep(15)


if __name__ == "__main__":
        main()

