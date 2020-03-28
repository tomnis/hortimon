import threading
import time


class BackgroundTask(object):

    __continue = True

    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    def __init__(self, hue, group, starting_brightness, time_minutes):
        """ Constructor
        """
        # in seconds
        interval_sec = time_minutes * 60.0 / starting_brightness
        transition_time_deci_sec = min(interval_sec, 10) * 10
        print("transition_time: %s" % transition_time_deci_sec)
        # start timer for interval

        def run_with_timer():
            hue.turn_group_off("tomas overhead lights")
            hue.set_light_group_temp("tomas lamps", 2000)
            current_brightness = starting_brightness
            hue.turn_group_on(group)

            hue.set_light_brightness('tomas sphere lamp', 5, transition_time_deci_sec / 2)

            while self.__continue and current_brightness > 0:
                hue.set_light_brightness('tomas lamp', current_brightness, transition_time_deci_sec / 2)
                time.sleep(interval_sec)
                current_brightness -= 1

            if current_brightness == 0:
                hue.turn_group_off(group)

        self.__thread = threading.Thread(target=run_with_timer, args=())
        self.__thread.daemon = True                            # Daemonize thread
        self.__thread.start()                                  # Start the execution

    def stop(self):
        self.__continue = False
        return True

