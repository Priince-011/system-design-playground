from .spot_state import SpotState
from .spot_type import SpotType
from .vehicle import Vehicle

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        self.id = spot_id
        self.type = spot_type
        self.state = SpotState.AVAILABLE
        self.parked_vehicle = None

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
        """Park a vehicle in this spot, enforcing invariants."""
        if not self.is_available():
            raise ValueError(f"Spot {self.id} is not available (state: {self.state})")
        if self.state == SpotState.OUT_OF_SERVICE:
            raise ValueError(f"Spot {self.id} is out of service")
        if not vehicle.can_park_in(self.type):
            raise ValueError(f"Vehicle {vehicle.get_registration_number()} is incompatible with spot type {self.type}")
        
        self.state = SpotState.OCCUPIED
        self.parked_vehicle = vehicle
    
    def free_parking_spot(self):
        """Free the parking spot after vehicle exit."""
        self.state = SpotState.AVAILABLE
        self.parked_vehicle = None
    
    def can_park_vehicle(self, vehicle: Vehicle):
        """Check if a vehicle can be parked in this spot."""
        return self.is_available() and vehicle.can_park_in(self.type)
