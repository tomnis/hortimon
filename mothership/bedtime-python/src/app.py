from flask import Flask
from hue_wrapper import HueWrapper
from background import BackgroundTask

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

    if background is not None:
        print("time in progress, stopping")
        background.stop()
    print "starting new task"
    background = BackgroundTask(hue, "tomas lamps", 30, 1)
    return 'started bed timer'


@app.route('/cancel')
def cancel():
    """

    should turn off lights in the group
    """
    #hue.turn_group_off(group)
    return "canceled"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
