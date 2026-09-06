from .vehicle import Vehicle
from .spot_type import SpotType
from .vehicle_size import VehicleSize

class Car(Vehicle):
    def __init__(self, registration_number: str, size: VehicleSize):
        super().__init__(registration_number, size)

    def can_park_in(self, spot_type):
        return spot_type in [SpotType.MEDIUM, SpotType.LARGE]
    