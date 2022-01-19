from models.bookingDemand import BookingDemand


class Room(object):
    def __init__(self, has_projector: bool, has_board: bool, chairs_num: int):
        self.has_projector = has_projector
        self.has_board = has_board
        self.chairs_num = chairs_num
        self.schedule = list()

    def book(self, room_demand: BookingDemand, team_id: int):
        if room_demand.is_complete:
            return True

        if room_demand.need_projector and not self.has_projector:
            return False

        for rd in self.schedule:
            if room_demand.overlap(rd[0]):
                return False

        self.schedule.append((room_demand, team_id))
        room_demand.is_complete = True
        return True
