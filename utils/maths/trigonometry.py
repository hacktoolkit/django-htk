# https://en.wikipedia.org/wiki/Trigonometry

import math

def deg2rad(degrees):
    """Degrees to radians
    """
    radians = math.pi * degrees/180.0
    return radians

def rad2deg(radians):
    """Radians to degrees
    """
    degrees = 180.0 * radians / math.pi
    return degrees

