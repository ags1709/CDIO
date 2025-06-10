

def get_speed_steering(self, steering, speed):
    """
    Calculate the speed_sp for each motor in a pair to achieve the specified
    steering. Note that calling this function alone will not make the
    motors move, it only calculates the speed. A run_* function must be called
    afterwards to make the motors move.

    steering [-100, 100]:
        * -100 means turn left on the spot (right motor at 100% forward, left motor at 100% backward),
        *  0   means drive in a straight line, and
        *  100 means turn right on the spot (left motor at 100% forward, right motor at 100% backward).

    speed:
        The speed that should be applied to the outmost motor (the one
        rotating faster). The speed of the other motor will be computed
        automatically.
    """

    assert steering >= -100 and steering <= 100,\
        "{} is an invalid steering, must be between -100 and 100 (inclusive)".format(steering)

    # We don't have a good way to make this generic for the pair... so we
    # assume that the left motor's speed stats are the same as the right
    # motor's.
    #speed = self.left_motor._speed_native_units(speed) # WARNING: idk this value lol
    left_speed = speed
    right_speed = speed
    speed_factor = (50 - abs(float(steering))) / 50

    if steering >= 0:
        right_speed *= speed_factor
    else:
        left_speed *= speed_factor

    return (left_speed, right_speed)


def tuple_toint(tuple):
    return (int(tuple[0]),int(tuple[1]))
    