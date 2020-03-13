from flask import Flask, render_template, request
from hue_wrapper import HueWrapper
from background import BackgroundTask

import logging
import json

logging.basicConfig()
app = Flask(__name__)
background = None


@app.route('/health-check')
def circle_wave():
    return render_template('circle_wave.html')


@app.route('/bedtime')
def student():
   return render_template('bedtime.html')

@app.route('/bedtimePost', methods = ['POST'])
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
    background = BackgroundTask(hue, "tomas lamps", starting_brightness, time_minutes)
    return 'started bed timer (brightness=%s, time_minutes=%sm)' % (starting_brightness, time_minutes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
