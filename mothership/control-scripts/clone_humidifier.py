from pyHS100 import SmartPlug
from plug_util import find_plug
from utils import retry
import argparse
from influxdb import InfluxDBClient
import os
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


def get_sleep_time(humidity):
    """
    Determines how long to humidify based on some arbitrary thresholds.

    :param humidity:
    :return:
    """
    if humidity > 65:
        return None
    elif humidity > 55:
        return 10
    else:
        return 20


@retry(Exception, tries=4)
def main():
    """
    Usage: run with arguments of the series and tag to check, and the ip address of the plug

    example:  >> python3 humidifier.py --environment clone.chamber --series humidity --plug-alias humidifier
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-s", "--series", help="influxdb series we are tracking")
    ap.add_argument("-p", "--plug-alias", help="alias of the smart plug")
    args = vars(ap.parse_args())

    environment = args.get("environment")
    series = args.get("series")
    plug_alias = args.get("plug_alias")

    value = current_value(series, environment)
    print("%s in %s: %s" % (series, environment, value))

    sleep_time = get_sleep_time(value)

    if sleep_time is None:
        print("humidity is high. not turning on humidifier")
    else:
        plug = find_plug(plug_alias)
        print("found plug on ip %s: %s" % (plug.ip_address, plug.alias))
        print("humidifying for %s seconds..." % sleep_time)
        plug.turn_on()
        time.sleep(sleep_time)
        plug.turn_off()
        print("done.")


if __name__ == "__main__":
    main()
