from enum import Enum

class StripeProductType(Enum):
    good = 1
    service = 2

class StripePlanInterval(Enum):
    day = 1
    week = 2
    month = 3
    year = 4
