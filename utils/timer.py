import time
from decimal import Decimal

class HtkTimer(object):
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()
        else:
            raise Exception('Timer has already started')

    def stop(self):
        if self.start_time is not None:
            if self.end_time is None:
                self.end_time = time.time()
            else:
                raise Exception('Timer has already stopped')
        else:
            raise Exception('Timer has not started yet')

    def duration(self, precision=2):
        if self.start_time is not None:
            if self.end_time is None:
                self.stop()
            duration = Decimal(self.end_time - self.start_time).quantize(Decimal(10) ** -precision)
        else:
            raise Exception('Timer has not started yet')
        return duration
