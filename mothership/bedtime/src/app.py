from flask import Flask, render_template, request
from hue_wrapper import HueWrapper
from bedtime_task import BedtimeTask

import logging
import json
import schedule
import time
import threading

logging.basicConfig()
app = Flask(__name__)
background = None
# traefik will route us on this prefix path (name of docker service) 
# TODO make this overridable
base_path = '/bedtime'


@app.route('/health-check')
def circle_wave():
    return render_template('circle_wave.html')


@app.route('/wake')
def wake():
    print("waking up")
    global background

    if background is not None:
        print("time in progress, stopping")
        background.stop()

    hue = HueWrapper("philips-hue.lan")
    # turn everything to 0 brightness and low temp
    hue.set_light_group_brightness("tomas overhead lights", 0)
    hue.set_light_group_brightness("tomas lamps", 0)
    print("set brightness=0")
    time.sleep(3)

    hue.set_light_group_temp("tomas overhead lights", 2000)
    hue.set_light_group_temp("tomas lamps", 2000)
    print("set temp=2000")
    time.sleep(3)
    hue.turn_group_on("tomas overhead lights")
    hue.turn_group_on("tomas lamps")
    print("turned lights on")

    transition_min = 1
    transition_deci_sec = transition_min * 60 * 10
    # set brightness with transition
    hue.set_light_group_brightness("tomas overhead lights", 100, transition_deci_sec)
    hue.set_light_group_brightness("tomas lamps", 100, transition_deci_sec)
    print("set brightness transition")
    # set temp with transition
    hue.set_light_group_temp("tomas overhead lights", 6000, transition_deci_sec)
    hue.set_light_group_temp("tomas lamps", 6000, transition_deci_sec)
    print("set temp transition")

    # turn everything on
    time.sleep(3)
    return 'started wake timer'



def turn_all_off():
    print("turning everything off")
    global background

    if background is not None:
        print("time in progress, stopping")
        background.stop()

    hue = HueWrapper("philips-hue.lan")
    hue.set_light_group_brightness("tomas overhead lights", 0)
    hue.set_light_group_brightness("tomas lamps", 0)
    hue.turn_group_off('tomas overhead lights')
    hue.turn_group_off('tomas lamps')
    time.sleep(3)

@app.route('/')
def student():
    global base_path
    return render_template('bedtime.html', base_path=base_path)

@app.route('/go', methods = ['POST'])
def bedtime():
    global background

    if background is not None:
        print("time in progress, stopping")
        background.stop()

    result = json.loads(json.dumps(request.form))
    starting_brightness = int(result[u'brightness'])
    # total duration of timer in minutes
    time_minutes = int(result[u'time_minutes'])
    print("starting new task (%s, %s)" % (starting_brightness, time_minutes))
    # sleep 60 seconds between transitions
    hue = HueWrapper("philips-hue.lan")
    background = BedtimeTask(hue, starting_brightness, time_minutes)
    return 'started bed timer (brightness=%s, time_minutes=%sm)' % (starting_brightness, time_minutes)


def cron():
    weekday_start = "09:00"
    weekend_start = "10:30"
    schedule.every().monday.at(weekday_start).do(lambda: wake())
    schedule.every().tuesday.at(weekday_start).do(lambda: wake())
    schedule.every().wednesday.at(weekday_start).do(lambda: wake())
    schedule.every().thursday.at(weekday_start).do(lambda: wake())
    schedule.every().friday.at(weekday_start).do(lambda: wake())
    schedule.every().saturday.at(weekend_start).do(lambda: wake())
    schedule.every().sunday.at(weekend_start).do(lambda: wake())

    schedule.every().day.at("14:30").do(lambda: turn_all_off())

    # just for testing
    #schedule.every(10).minutes.do(lambda: wake())
    #schedule.every(5).minutes.do(lambda: turn_all_off())

    while True:
        schedule.run_pending()
        time.sleep(5)

    # TODO turn off lights at 3pm?


if __name__ == '__main__':
    c = threading.Thread(target=cron)
    c.daemon = True  # Daemonize thread
    c.start()  # Start the execution

    app.run(debug=True, host='0.0.0.0')
