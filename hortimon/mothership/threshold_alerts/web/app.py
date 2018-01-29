from flask import Flask
app = Flask(__name__)
from flask import request

import json
import os
import sys

path =  "../../notifier"
sys.path.append(os.path.abspath(path))

from TwilioNotifier import *

@app.route('/')
def hello_world():
    """
    Just a simple test page. We can navigate to http://localhost:5000 in the browser.
    """
    return 'sms-notifier running in docker'


@app.route('/send-sms', methods=['POST'])
def send_sms():
    """
    Sends sms notifications to the numbers in the environment variable twilio_notify_to
    """
    json_event = json.loads(request.data)
    message = json_event["message"]
    print("parsed message:" + str(message))
    to_numbers = os.environ['twilio_notify_to'].split(',')

    for number in to_numbers:
        print("sending sms to " + number)
        TwilioNotifier.send_sms(number, message)

    return "ok"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
