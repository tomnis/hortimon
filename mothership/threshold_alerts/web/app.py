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


def internal_send_sms(message, to_numbers):
    """
    Sends given message to the each number in the list.
    """
	
    for number in to_numbers:
        print("sending sms to " + number)
        TwilioNotifier.send_sms(number, message)

    return "messages sent: " + str(len(to_numbers))
    

@app.route('/send-sms', methods=['POST'])
def send_sms():
    """
    Sends sms notifications to the comma-separated numbers in the request body field "to_numbers".
    """
    json_event = json.loads(request.data)
    message = json_event["message"]
    to_numbers = json_event["to_numbers"].split(',')
    print("parsed message:" + str(message))

    return internal_send_sms(message, to_numbers)


@app.route('/send-sms-to-env', methods=['POST'])
def send_sms_to_env():
    """
    Sends sms notifications to the comma-separated numbers in the environment var TWILIO_NOTIFY_TO.
    """
    json_event = json.loads(request.data)
    message = json_event["message"]
    to_numbers = os.environ["TWILIO_NOTIFY_TO"].split(',')
    print("parsed message:" + str(message))

    return internal_send_sms(message, to_numbers)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
