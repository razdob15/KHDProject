from datetime import datetime

from models.bookingDemand import BookingDemand


class Team(object):
    def __init__(self, preferred_rooms: list):
        """
        A team in a troop.
        :param preferred_rooms: A of the preferred rooms for the team in a descending order.
        """
        self.preferred_rooms = preferred_rooms
        self.booking_remands = list()

    def demand_booking(self, room_demand: BookingDemand):
        print("Book demand to my team!")
        for rd in self.booking_remands:
            if room_demand.overlap(rd):
                return False

        self.booking_remands.append(room_demand)
        return True
