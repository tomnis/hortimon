from pyHS100 import SmartPlug
import argparse
from influxdb import InfluxDBClient
from plug_util import find_plug_ip_address, set_plug
import os
import requests
import time


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
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-s", "--series", help="influxdb series we are tracking")
    ap.add_argument("-p", "--plug-alias", help="alias of the smart plug")
    ap.add_argument("-t", "--target-temperature", help="target temperature of the environment")
    ap.add_argument("-n", "--to-numbers", help="comma separated numbers to send notifications to")
    args = vars(ap.parse_args())

    plug_alias = args.get("plug_alias")
    plug_ip = find_plug_ip_address(plug_alias)

    try:
        target_temperature = float(args.get("target_temperature"))
        print("target temperature is: %s" % (target_temperature))
            
        environment = args.get("environment")
        series = args.get("series")
    
        current_temperature = current_value(series, environment)
        print("%s in %s: %s" % (series, environment, current_temperature))
    
        dry_run = args.get("dry_run")
        to_numbers = args.get("to_numbers")
    
        # if its already cool enough, turn off the ac
        if target_temperature > current_temperature:
            print("current temperature is low . ac should be off.")
            if not dry_run:
                state_changed = set_plug(plug_ip, False)
                #if state_changed:
                #    send_notifications("turned off ac (current=%s, target=%s)" % (current_temperature, target_temperature), to_numbers)
            else:
                print("running in dry run mode")
        else:
            print("current temperature is warm. ac should be on.")
            if not dry_run:
                state_changed = set_plug(plug_ip, True)
                #if state_changed:
                #    send_notifications("turned on ac (current=%s, target=%s)" % (current_temperature, target_temperature), to_numbers)
            else:
                print("running in dry run mode")
    except Exception as err:
        print(err)
        dry_run = args.get("dry_run")
        if not dry_run:
            print("something went wrong, turn on ac")
            send_notification("error %s" % err)
            set_plug(plug_ip, True)


if __name__ == "__main__":
    main()
