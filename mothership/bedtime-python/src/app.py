from flask import Flask
from hue_wrapper import HueWrapper
from background import BackgroundTask

import logging

logging.basicConfig()
app = Flask(__name__)
background = None


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/bedtime')
def bedtime():
    global background
    hue = HueWrapper("philips-hue.lan")
    hue.turn_group_off("tomas overhead lights")
    hue.set_light_group_temp("tomas lamps", 2000)

    if background is not None:
        print("time in progress, stopping")
        background.stop()
    print "starting new task"
    # sleep 60 seconds between transitions
    background = BackgroundTask(hue, "tomas lamps", 40, 60)
    return 'started bed timer'


@app.route('/test')
def test():
    hue = HueWrapper("philips-hue.lan")
    hue.set_light_group_temp("Upstairs Room", 4000)

    return 'set light color temp'

@app.route('/cancel')
def cancel():
    """

    should turn off lights in the group
    """
    #hue.turn_group_off(group)
    return "canceled"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
