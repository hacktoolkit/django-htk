# Python Standard Library Imports
import math


def quadratic(a, b, c):
    """Solves the quadratic equation
    ax^2 + b + c = 0
    (-b + sqrt(b^2 - 4ac)) / 2a
    """
    x = (math.sqrt((b * b) - (4 * a * c)) - b) / (2 * a)
    return x
