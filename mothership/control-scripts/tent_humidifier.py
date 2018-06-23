from datetime import datetime

from pyHS100 import SmartPlug
from influxdb import InfluxDbClient
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

    if current_humidity > 75:
        return None
    elif 11 <= hour <= 19:
        return 20
    elif current_humidity > 50:
        return 120
    else:
        return 180


def main():
    """
    Usage: run with arguments of the series, environment, and the ip address of the plug we should turn on.

    example:  >> python3 tent_humidifier.py --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-s", "--series", help="influxdb series we are tracking")
    ap.add_argument("-p", "--plug", help="ip address of the smart plug")
    args = vars(ap.parse_args())

    plug_ip = args.get("plug")
    series = args.get("series")
    environment = args.get("environment")

    humidify_time = get_sleep_time(series, environment)
    print("going to humidify for %s" % humidify_time)

    if humidify_time is not None:
        plug = SmartPlug(plug_ip)
        print("found plug on ip %s: %s" % (plug_ip, plug.alias))
        plug.turn_on()
        time.sleep(int(humidify_time))
        plug.turn_off()


if __name__ == "__main__":
    main()
