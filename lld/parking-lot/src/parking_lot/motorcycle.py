from .vehicle import Vehicle
from .vehicle_type import VehicleType
from .vehicle_size import VehicleSize


class Motorcycle(Vehicle):
    """Motorcycle: small vehicle."""
    
    def __init__(self, registration_number: str, size: VehicleSize = VehicleSize.SMALL):
        super().__init__(registration_number, VehicleType.MOTORCYCLE, size)
