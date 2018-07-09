from pyHS100 import SmartPlug, Discover


def find_plug(alias):
    """
    Finds the plug with the given alias
    """
    return next(device for device in Discover.discover().values() if device.alias == alias)



def find_plug_ip_address(alias):
    """"
    Finds the ip address of the plug with the given alias.
    """
    return find_plug(alias).ip_address



def set_plug(plug_ip, value):
    """
    Sets the plug at the given ip to the given value.
    Returns true iff the plug had a state change.
    """
    plug = SmartPlug(plug_ip)
    print("found plug on ip %s: %s" % (plug_ip, plug.alias))
    state = plug.state
    print("current plug state: " + str(state))
    if value and not plug.is_on:
        print("turning on fan")
        plug.turn_on()
        return True
    elif not value and plug.is_on:
        print("turning off fan")
        plug.turn_off()
        return True
    else:
        print("plug is already in correct state")
        return False
