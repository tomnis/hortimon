from flask import Flask, render_template, request
from hue_wrapper import HueWrapper
from bedtime_task import BedtimeTask
from wakeup_task import WakeupTask

import logging
import json

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
    hue = HueWrapper("philips-hue.lan")
    a = WakeupTask(hue, time_minutes=1.0)
    return 'started wake timer'


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
