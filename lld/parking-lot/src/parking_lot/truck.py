from .vehicle import Vehicle
from .vehicle_type import VehicleType
from .vehicle_size import VehicleSize


class Truck(Vehicle):
    """Truck: large vehicle."""
    
    def __init__(self, registration_number: str, size: VehicleSize = VehicleSize.LARGE):
        super().__init__(registration_number, VehicleType.TRUCK, size)
