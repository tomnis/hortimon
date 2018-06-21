from pyHS100 import SmartPlug
import argparse
from influxdb import InfluxDBClient
import openweathermapy.core as owm
import os
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
    ap.add_argument("-p", "--plug", help="ip address of the smart plug")
    args = vars(ap.parse_args())

    location = args.get("location")
    outdoor_temperature = current_temperature(location)
    print("outdoor_temperature in %s: %s" % (location, outdoor_temperature))
        
    environment = args.get("environment")
    series = args.get("series")
    plug_ip = args.get("plug")

    indoor_temperature = current_value(series, environment)
    print("%s in %s: %s" % (series, environment, indoor_temperature))

    dry_run = args.get("dry_run")

    # if its too hot outside, we don't want to bring the hot air in
    if outdoor_temperature > indoor_temperature:
        print("outdoor temperature is high. fan should be off.")
        if not dry_run:
            print("turning off fan...")
            plug = SmartPlug(plug_ip)
            print("found plug on ip %s: %s" % (plug_ip, plug.alias))
            plug.turn_off()
        else:
            print("running in dry run mode")
    else:
        print("outdoor temperature is cool. fan should be on.")
        if not dry_run:
            print("turning on fan...")
            plug = SmartPlug(plug_ip)
            print("found plug on ip %s: %s" % (plug_ip, plug.alias))
            plug.turn_on()
        else:
            print("running in dry run mode")


if __name__ == "__main__":
    main()
