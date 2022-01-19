from datetime import datetime


class Booking(object):
    def __init__(self, start_time: datetime, end_time: datetime, need_projector: bool):
        self.start_time = start_time
        self.end_time = end_time
        self.need_projector = need_projector

    def __str__(self):
        return self.start_time.strftime('%H%M') + self.end_time.strftime('%H%M')

    def overlap(self, other):
        return self.start_time <= other.start_time < self.end_time or \
               self.start_time < other.end_time <= self.end_time \
               or (other.start_time <= self.start_time and other.end_time >= self.end_time)
