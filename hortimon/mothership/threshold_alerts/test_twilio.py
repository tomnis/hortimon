#!/usr/bin/python

import os
import sys

path =  "../notifier"
sys.path.append(os.path.abspath(path))

from TwilioNotifier import *

def main():
    """
    A simple test using our twilio wrapper.
    """

    twilio_to = os.environ['twilio_test_to']
    TwilioNotifier.send_sms(twilio_to, "hi this is your master")

if __name__ == "__main__":
    main()
