from datetime import datetime

from pyHS100 import SmartPlug
import argparse
import pytz
import time


def get_sleep_time():
    """
    :return: the amount of time (in seconds) that we should sleep for.
    """
    hour = datetime.now(pytz.timezone('US/Pacific')).hour

    if 11 <= hour <= 17:
        return 20
    else:
        return 180


def main():
    """
    Usage: run with arguments of the time to mist for, and the ip address of the plug

    example:  >> python3 mister.py --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--plug", help="ip address of the smart plug")
    args = vars(ap.parse_args())

    plug_ip = args.get("plug")

    mist_time = get_sleep_time()
    print("going to mist for %s" % mist_time)

    plug = SmartPlug(plug_ip)
    print("found plug on ip %s: %s" % (plug_ip, plug.alias))
    plug.turn_on()
    time.sleep(int(mist_time))
    plug.turn_off()


if __name__ == "__main__":
    main()