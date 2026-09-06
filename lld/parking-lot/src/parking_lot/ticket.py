import uuid
import time
from .vehicle import Vehicle
from .parking_spot import ParkingSpot

class Ticket:
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot):
        self.id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.entry_timestamp = int(time.time()*1000)  # Store entry time in milliseconds
        self.exit_timestamp = None

    def get_id(self):
        return self.id
    
    def get_vehicle(self):
        return self.vehicle
    
    def get_parking_spot(self):
        return self.parking_spot
    
    def get_entry_timestamp(self):
        return self.entry_timestamp
    
    def get_exit_timestamp(self):
        return self.exit_timestamp
    
    def set_exit_timestamp(self):
        self.exit_timestamp = int(time.time()*1000)  # Store exit time in milliseconds