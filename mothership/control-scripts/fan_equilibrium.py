from pyHS100 import SmartPlug
import argparse
from influxdb import InfluxDBClient
from plug_util import find_plug_ip_address, set_plug
import openweathermapy.core as owm
import os
import requests
import time


open_weather_map_key = os.environ["OPEN_WEATHER_MAP_KEY"]
settings = {"units": "imperial", "APPID": open_weather_map_key}


def current_temperature(location):
    """
    Checks outdoor temperature in the specified location.

    See https://pypi.python.org/pypi/openweathermapy/0.6.6

    :param location: zip code or city to check for current conditions.
    :return: current humidity in the specified location.
    """
    data = owm.get_current(location, **settings)
    return data["main"]["temp"]


def current_value(series, environment):
    """
    Checks current value in the given influxdb series


    :param series: series to check
    :param environment: tag to check
    :return: current value in the given series
    """
    client = InfluxDBClient('hortimon-mothership.local', 8086, 'root', 'root', 'garden')
    query = """select %s from garden where time > now() - 1m and  "environment"='%s'""" % (series, environment)

    result = client.query(query)
    return list(result.get_points())[0][series]


def send_notifications(message, to_numbers):
    post_data = {
            "message" : message,
            "to_numbers" : to_numbers
            }

    print(post_data)
    post_url = "http://localhost:5000/send-sms"
    r = requests.post(post_url, json=post_data)
    print("POST to notifier server response: " + str(r.status_code))
    return r

def main():
    """
    Usage: run with arguments of the series and tag to check, and the ip address of the plug

    example:  >> python3 fan_equilibrium.py --environment <tag> --series <series> --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dry-run", help="whether to treat this as a dry run", type=bool, default=False)
    ap.add_argument("-l", "--location", help="zip code or city for weather conditions")
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-s", "--series", help="influxdb series we are tracking")
    ap.add_argument("-p", "--plug-alias", help="alias of the smart plug")
    ap.add_argument("-n", "--to-numbers", help="comma separated numbers to send notifications to")
    args = vars(ap.parse_args())

    plug_alias = args.get("plug_alias")
    plug_ip = find_plug_ip_address(plug_alias)
    location = args.get("location")

    try:
        outdoor_temperature = current_temperature(location)
        print("outdoor temperature in %s: %s" % (location, outdoor_temperature))
            
        environment = args.get("environment")
        series = args.get("series")
    
        indoor_temperature = current_value(series, environment)
        print("%s in %s: %s" % (series, environment, indoor_temperature))
    
        dry_run = args.get("dry_run")
        to_numbers = args.get("to_numbers")
    
        # if its too hot outside, we don't want to bring the hot air in
        if outdoor_temperature > indoor_temperature:
            print("outdoor temperature is high. fan should be off.")
            if not dry_run:
                state_changed = set_plug(plug_ip, False)
                if state_changed:
                    send_notifications("turned off intake fan (outdoor=%s, indoor=%s)" % (outdoor_temperature, indoor_temperature), to_numbers)
            else:
                print("running in dry run mode")
        else:
            print("outdoor temperature is cool. fan should be on.")
            if not dry_run:
                state_changed = set_plug(plug_ip, True)
                if state_changed:
                    send_notifications("turned on intake fan (outdoor=%s, indoor=%s)" % (outdoor_temperature, indoor_temperature), to_numbers)
            else:
                print("running in dry run mode")
    except Exception as err:
        print(err)
        if not dry_run:
            print("something went wrong, turn on fans")
            set_plug(plug_ip, True)


if __name__ == "__main__":
    main()
