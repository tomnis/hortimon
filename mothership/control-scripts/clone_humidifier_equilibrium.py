from pyHS100 import SmartPlug
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
    print(query)

    result = client.query(query)
    print(result)
    return list(result.get_points())[0][series]


def get_sleep_time(humidity):
    """
    Determines how long to humidify based on some arbitrary thresholds.

    :param humidity:
    :return:
    """
    if humidity > 75:
        return None
    elif humidity > 60:
        return 15
    else:
        return 20


def main():
    """
    Usage: run with arguments of the series and tag to check, and the ip address of the plug

    example:  >> python3 humidifier.py --environment clone.chamber --series humidity --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-s", "--series", help="influxdb series we are tracking")
    ap.add_argument("-p", "--plug", help="ip address of the smart plug")
    args = vars(ap.parse_args())

    environment = args.get("environment")
    series = args.get("series")
    plug_ip = args.get("plug")

    value = current_value(series, environment)
    print("%s in %s: %s" % (series, environment, value))

    sleep_time = get_sleep_time(value)

    if sleep_time is None:
        print("humidity is high. not turning on humidifier")
    else:
        print("humidifying for %s seconds" % sleep_time)
        plug = SmartPlug(plug_ip)
        print("found plug on ip %s: %s" % (plug_ip, plug.alias))
        plug.turn_on()
        time.sleep(sleep_time)
        plug.turn_off()


if __name__ == "__main__":
    main()
