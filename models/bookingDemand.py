from models.booking import Booking
from datetime import datetime


class BookingDemand(Booking):
    def __init__(self, start_time: datetime, end_time: datetime, need_projector: bool):
        super().__init__(start_time, end_time, need_projector)
        self.is_complete = False
