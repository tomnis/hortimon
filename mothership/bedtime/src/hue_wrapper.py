from phue import Bridge


class HueWrapper:

    def __init__(self, bridge_ip):
        """

        :param bridge_ip: ip address of the hue bridge
        """
        self.bridge = Bridge(bridge_ip)
        # first time we run, we have to press the physical button on the bridge device
        self.bridge.connect()

        lights = self.bridge.lights

        # Print light names
        print("found the following lights on bridge {}".format(bridge_ip))
        for l in lights:
            print(l.name)

    def is_group_on(self, group):
        """
        Checks whether the specified group is on.

        :param group:
        :return: True iff the specified group is on.
        """
        return self.bridge.get_group(group, "on")

    def turn_group_off(self, group):
        """
        Turns off the specified group.

        :param group:
        :return:
        """
        self.bridge.set_group(group, "on", False)

    def turn_group_on(self, group):
        """
        Turns on the specified group.

        :param group:
        :param transition_time: slow transition
        :return:
        """
        self.bridge.set_group(group, "on", True)

    def set_light_group_brightness(self, group, brightness_pct, transition_time=None):
        """
        Sets the brightness for the specified light group.

        Note that setting brightness to 0 will not turn off the light.

        :param group:
        :param brightness_pct:
        :return:
        """
        self.bridge.set_group(group, 'bri', self.brightness_from_pct(brightness_pct), transition_time)

    '''Get or set the color temperature of the light, in units of Kelvin [2000-6500]'''
    def set_light_group_temp(self, group, temp, transition_time=None):
        mireds = int(round(1e6 / temp))
        self.bridge.set_group(group, 'ct', mireds, transition_time)

    def set_light_brightness(self, light, brightness_pct, transition_time=None):
        """
        Sets the brightness for the specified light.

        Note that setting brightness to 0 will not turn off the light.

        :param light:
        :param brightness_pct:
        :param transition_time:
        :return:
        """
        self.bridge.set_light(light, 'bri', self.brightness_from_pct(brightness_pct), transitiontime=transition_time)

    def turn_light_on(self, light):
        self.bridge.set_light(light, 'on', True)

    def turn_light_off(self, light):
        self.bridge.set_light(light, 'on', False)

    @staticmethod
    def brightness_from_pct(brightness_pct):
        """
        Converts an integer representing percentage into a value acceptable for hue api

        :param brightness_pct:
        :return:
        """
        return int(float(brightness_pct) / 100 * 254)

