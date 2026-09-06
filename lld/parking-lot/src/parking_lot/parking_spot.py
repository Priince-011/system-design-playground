from .spot_state import SpotState
from .spot_type import SpotType
from .vehicle import Vehicle

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        self.id = spot_id
        self.type = spot_type
        self.state = SpotState.AVAILABLE

    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def get_state(self):
        return self.state
    
    def is_available(self):
        return self.state == SpotState.AVAILABLE
    
    def is_occupied(self):
        return self.state == SpotState.OCCUPIED
    
    def park_vehicle(self, vehicle: Vehicle):
        self.state = SpotState.OCCUPIED
        self.parked_vehicle = vehicle
    
    def free_parking_spot(self):
        self.state = SpotState.AVAILABLE
        self.parked_vehicle = None
    
    def can_park_vehicle(self, vehicle: Vehicle):
        return self.is_available() and vehicle.can_park_in()
    
    