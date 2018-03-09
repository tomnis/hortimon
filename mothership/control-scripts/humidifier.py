from pyHS100 import SmartPlug
import argparse
import openweathermapy.core as owm
import os
import time

open_weather_map_key = os.environ["OPEN_WEATHER_MAP_KEY"]
settings = {"units": "imperial", "APPID": open_weather_map_key}


def current_humidity(location):
    """
    Checks humidity in the specified location.

    See https://pypi.python.org/pypi/openweathermapy/0.6.6

    :param location: zip code or city to check for current conditions.
    :return: current humidity in the specified location.
    """
    data = owm.get_current(location, **settings)
    return data["main"]["humidity"]


def get_sleep_time(humidity):
    """
    Determines how long to humidify based on some arbitrary thresholds.

    :param humidity:
    :return:
    """
    if humidity > 90:
        return None
    elif humidity > 80:
        return 30
    elif humidity > 70:
        return 120
    elif humidity > 60:
        return 320
    else:
        return 600


def main():
    """
    Usage: run with arguments of the zip code or city to check humidity in, and the ip address of the plug

    Make sure to export OPEN_WEATHER_MAP_KEY as an environment variable.

    example:  >> python3 humidifier.py --location mordor --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--location", help="zip code or city for weather conditions")
    ap.add_argument("-p", "--plug", help="ip addresss of the smart plug")
    args = vars(ap.parse_args())

    location = args.get("location")
    plug_ip = args.get("plug")

    humidity = current_humidity(location)
    print("humidity in %s: %s" % (location, humidity))

    sleep_time = get_sleep_time(humidity)

    if sleep_time is None:
        print("humidity is high. is it raining? not turning on humidifier")
    else:
        print("humidifying for %s seconds" % sleep_time)
        plug = SmartPlug(plug_ip)
        print("found plug on ip %s: %s" % (plug_ip, plug.alias))
        plug.turn_on()
        time.sleep(sleep_time)
        plug.turn_off()


if __name__ == "__main__":
    main()