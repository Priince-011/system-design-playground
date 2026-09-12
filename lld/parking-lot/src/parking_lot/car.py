from .vehicle import Vehicle
from .vehicle_type import VehicleType
from .vehicle_size import VehicleSize


class Car(Vehicle):
    """Car: medium vehicle."""
    
    def __init__(self, registration_number: str, size: VehicleSize = VehicleSize.MEDIUM):
        super().__init__(registration_number, VehicleType.CAR, size)
