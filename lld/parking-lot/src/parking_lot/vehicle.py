from abc import ABC, abstractmethod
from .spot_type import SpotType
from .vehicle_size import VehicleSize

class Vehicle(ABC):
    def __init__(self, registration_number: str, size: VehicleSize):
        self.regn_no = registration_number
        self.size = size

    @abstractmethod
    def can_park_in(self, spot_type: SpotType):
        pass

    def get_registration_number(self):
        return self.regn_no