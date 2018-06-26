from datetime import datetime
from plug_util import find_plug
from pyHS100 import SmartPlug
from influxdb import InfluxDBClient
import argparse
import pytz
import time


def current_value(series, environment):
    """
    Checks current value in the given series
    :param series: series to check
    :param environment: tag to check
    :return: current value in the given series
    """
    client = InfluxDBClient('hortimon-mothership.local', 8086, 'root', 'root', 'garden')
    query = """select %s from garden where time > now() - 1m and  "environment"='%s'""" % (series, environment)

    result = client.query(query)
    return list(result.get_points())[0][series]


def get_sleep_time(series, environment):
    """
    :return: the amount of time (in seconds) that we should sleep for. could be None if its already humid enough.
    """
    hour = datetime.now(pytz.timezone('US/Pacific')).hour
    current_humidity = current_value(series, environment)

    if current_humidity > 65:
        return None
    elif 11 <= hour <= 19:
        return None
    elif current_humidity > 50:
        return 110
    else:
        return 180


def main():
    """
    Usage: run with arguments of the series, environment, and the ip address of the plug we should turn on.

    example:  >> python3 tent_humidifier.py --plug-alias humidifier-01
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-s", "--series", help="influxdb series we are tracking")
    ap.add_argument("-p", "--plug-alias", help="alias of the smart plug")
    args = vars(ap.parse_args())

    plug_alias = args.get("plug_alias")
    series = args.get("series")
    environment = args.get("environment")

    humidify_time = get_sleep_time(series, environment)
    print("going to humidify for %s" % humidify_time)

    if humidify_time is not None:
        plug = find_plug(plug_alias)
        print("found plug on ip %s: %s" % (plug.ip_address, plug.alias))
        plug.turn_on()
        time.sleep(int(humidify_time))
        plug.turn_off()


if __name__ == "__main__":
    main()
