#!/usr/bin/python3

import argparse
from plug_util import filter_plugs_by_prefix, set_plug
import openweathermapy.core as owm
import os
import schedule
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


def itr(location, plug_prefix):

    outdoor_temp = current_temperature(location)
    print("current temp in: " + str(location) + ": " + str(outdoor_temp))
    fans_state = outdoor_temp < 75
    print("desired fan state: " + str(fans_state))
    for plug_ip in filter_plugs_by_prefix(plug_prefix):
        set_plug(plug_ip, fans_state)


def main():
    """
    Usage: run with arguments of the plug common prefix name to control. pyHS100 doesnt seem to support groups.

    example:  >> python3 fan_equilibrium.py --plug-prefix LR_intakes
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--plug-prefix", help="prefix of the smart plugs alias")
    args = vars(ap.parse_args())

    location = os.environ["ZIP_CODE"]
    plug_prefix = args.get("plug_prefix")
    print(plug_prefix)

    schedule.every(5).minutes.do(lambda: itr(location, plug_prefix))

    while True:
        schedule.run_pending()
        time.sleep(30)



if __name__ == "__main__":
    main()