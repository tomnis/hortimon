#!/usr/bin/python3

from datetime import datetime
from pyHS100 import SmartPlug
import argparse
from influxdb import InfluxDBClient
from plug_util import find_plug_ip_address, set_plug
import os
import requests
import schedule
import time
import pytz


def current_value(environment):
    """
    Checks current value in the given influxdb series


    :param environment: tag to check
    :return: current value in the given series
    """
    client = InfluxDBClient(host='isengard.lan', port=80, path='/influxdb',  username='root', password='root', database='garden')
    query = """select temperature from garden where time > now() - 1m and  "environment"='%s'""" % (environment)

    result = client.query(query)
    return list(result.get_points())[0]["temperature"]


def itr(dry_run, environment, plug_ip, max_temp):
    current_temp = current_value(environment)
    print(current_temp)

    if (current_temp > max_temp):
        if not dry_run:
            state_changed = set_plug(plug_ip, True)
    else:
        if not dry_run:
            state_changed = set_plug(plug_ip, False)


def main():
    """
    Usage: run with arguments of the series and tag to check, and the ip address of the plug

    example:  >> python3 fan_equilibrium.py --environment <tag> --series <series> --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dry-run", help="whether to treat this as a dry run", type=bool, default=False)
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-p", "--plug-alias", help="alias of the smart plug")
    ap.add_argument("-t", "--max-temperature", help="max temperature of the environment", type=float)
    ap.add_argument("-n", "--to-numbers", help="comma separated numbers to send notifications to")
    args = vars(ap.parse_args())

    dry_run = args.get("dry_run")
    environment = args.get("environment")
    plug_alias = args.get("plug_alias")
    max_temp = args.get("max_temperature")
    print("plug_alias: " + plug_alias)
    plug_ip = find_plug_ip_address(plug_alias)
    print("plug_ip: " + plug_ip)

    schedule.every(30).seconds.do(lambda: itr(dry_run, environment, plug_ip, max_temp))

    while True:
        schedule.run_pending()
        time.sleep(30)



if __name__ == "__main__":
    main()
