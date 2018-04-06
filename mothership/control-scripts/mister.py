from pyHS100 import SmartPlug
import argparse
import time


def main():
    """
    Usage: run with arguments of the time to mist for, and the ip address of the plug

    example:  >> python3 mister.py --time 10 --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--time", help="duration to mist for (seconds)")
    ap.add_argument("-p", "--plug", help="ip address of the smart plug")
    args = vars(ap.parse_args())

    mist_time = args.get("time")
    plug_ip = args.get("plug")

    print("going to mist for %s" % mist_time)

    plug = SmartPlug(plug_ip)
    print("found plug on ip %s: %s" % (plug_ip, plug.alias))
    plug.turn_on()
    time.sleep(int(mist_time))
    plug.turn_off()


if __name__ == "__main__":
    main()