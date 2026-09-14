from abc import ABC
from .vehicle_type import VehicleType
from .vehicle_size import VehicleSize


class Vehicle(ABC):
    """Abstract base class for vehicles.
    
    Vehicles describe themselves: type, size, registration.
    They do NOT decide where they can park.
    ParkingSpot determines compatibility based on size.
    """
    
    def __init__(self, registration_number: str, vehicle_type: VehicleType, size: VehicleSize):
        self.regn_no = registration_number
        self.vehicle_type = vehicle_type
        self.size = size

    def get_registration_number(self) -> str:
        return self.regn_no
    
    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type
    
    def get_size(self) -> VehicleSize:
        return self.size
