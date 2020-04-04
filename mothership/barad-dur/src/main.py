#!/usr/bin/python3
# loop over the video frames

# check for motion
# if the light is off:

#   if there is motion, run the person detector

#       if there is a person
#           turn on the lights.
#           the brightness should be a function of the time of day, including sunset/sunrise time
#           sleep for a certain amount of time. this should also be a function of the time of day

# if the light is on:
#   if there is motion, run the person detector:
#       if there is a person, keep the lights on and sleep
#       otherwise, turn the lights off and don't sleep
#

from hue.hue_wrapper import HueWrapper
from optics.human_detector import HumanDetector
from optics.motion_detector import MotionDetector
from model.hue_strategy import HueStrategy
from model.hue_state_change import HueStateChangeEvent
from picamera.array import PiRGBArray
from util.storm import getSunrise, getSunset
from picamera import PiCamera

import cv2
import datetime
import pytz
import sys
import time


last_off_time = time.time()


def get_camera():
    """
    Connects to the camera

    :return: a handle to the camera and its capture feed
    """
    resolution = (640, 480)
    camera = PiCamera()
    camera.resolution = resolution
    # TODO overclock
    camera.framerate = 12
    camera.contrast = 70
    camera.brightness = 80
    camera.iso = 800
    raw_capture = PiRGBArray(camera, size=resolution)
    raw_capture.truncate(0)
    raw_capture.seek(0)
    # warmup the sensor array
    time.sleep(3)
    return (camera, raw_capture)


def scan(camera, capture, hue, strategy):
    """
    Scans the video stream for motion and humans.

    :param camera:
    :param capture:
    :param hue:
    :param strategy:
    :return:
    """
    global last_off_time
    human_detector = HumanDetector()
    motion_detector = MotionDetector(min_area=900)
    human_threshold = 0.3

    print("scanning video stream...")
    stream = camera.capture_continuous(capture, format="bgr", use_video_port=True)

    # discard the first few frames
    for i in range(16):
        next(stream)
        capture.truncate(0)

    previous_frame = next(stream).array
    capture.truncate(0)

    for frame in stream:
        frame = frame.array

        # first check for motion
        motion_rects = list(motion_detector.detect(previous_frame, frame))
        if len(motion_rects) > 0:
            print("found motion {}".format(motion_rects))

            # the lights are already on and we found motion. leave them on and go back to sleep.
            # its too slow to rely on the person detector here
            if hue.is_group_on(strategy.hue_group):
                break

            # if we found motion, continue by checking for humans
            (human_rects, human_weights) = human_detector.detect(frame)
            print("human weights: {}".format(human_weights))

            # filter on a small threshold to avoid false positives
            filtered_weights = filter(lambda w: w > human_threshold, human_weights)
            # TODO we should also check that the rects are overlapping
            if len(list(filtered_weights)) > 0:
                brightness = strategy.brightness()
                print \
                    ("found humans above threshold {}, turning on {} lights, brightness={}".format(human_threshold, strategy.hue_group, brightness))
                hue.turn_group_on(strategy.hue_group)
                hue.set_light_group_brightness(strategy.hue_group, brightness)
                break
            # just print that we are likely avoiding a false positive
            elif len(human_rects) > 0:
                print("found humans below threshold {} (likely false positive)".format(human_threshold))

        elif hue.is_group_on(strategy.hue_group):
            (human_rects, human_weights) = human_detector.detect(frame)
            print("human weights: {}".format(human_weights))
            # filter on a smaller threshold to avoid false positives
            filtered_weights = filter(lambda w: w > human_threshold * 0.75, human_weights)
            print("turning off {} lights".format(strategy.hue_group))
            if len(list(filtered_weights)) == 0:
                hue.turn_group_off(strategy.hue_group)
                last_off_time = time.time()

        previous_frame = frame
        # we need to truncate the buffer before the next iteration
        capture.truncate(0)
        capture.seek(0)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            sys.exit(1)

    return HueStateChangeEvent(strategy.sleep_when_on)


def get_brightness():
    """
    :return: the brightness we should set the lights to based on time of day.
    """
    hour = datetime.datetime.now(pytz.timezone('US/Pacific')).hour

    sunrise = getSunrise()
    sunset = getSunset()


    # late night
    if hour <= 3:
        return 20
    # late night
    elif hour <= 5:
        return 20
    # early morning
    elif hour <= sunrise[0]:
        return 100
    # during work
    elif hour <= 18:
        return 50
    elif hour <= sunset[0]:
        return 100
    else:
        return 80


def get_sleep_time(last_off_time):
    """
    TODO this should lookup sunrise and sunset time
    TODO this should return a tuple and be combined with get_brightness()
    :return: the amount of time (in seconds) that we should sleep for after turning the lights on.
    """
    hour = datetime.datetime.now(pytz.timezone('US/Pacific')).hour
    epoch_seconds = time.time()
    sleep_time = None
    # late night
    if hour <= 3:
        sleep_time = 600
    # sleep time
    elif hour <= 7:
        sleep_time = 120
    else:
        sleep_time = 600

    if (epoch_seconds - last_off_time) < 10:
        print("extending time, someone is probably cooking")
        return sleep_time * 3
    else:
        return sleep_time


def main():
    """
    Main script loop.

    Creates a hue wrapper and monitors the video stream.
    :return:
    """
    global last_off_time
    hue = HueWrapper("philips-hue.lan")

    last_off_time = time.time()

    (camera, capture, result) = None, None, None

    while True:
        # create a camera
        (camera, capture) = get_camera()
        # create a strategy
        strategy = HueStrategy("Kitchen", lambda: get_brightness(), lambda: get_sleep_time(last_off_time))
        # scan the video stream
        result = scan(camera, capture, hue, strategy)
        camera.close()
        capture.close()
        print("sleeping for {}s".format(result.sleep_time()))
        time.sleep(result.sleep_time())

if __name__ == "__main__":
    main()
