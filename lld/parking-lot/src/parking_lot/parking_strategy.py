from abc import ABC, abstractmethod
from typing import List, Optional
from .parking_floor import ParkingFloor
from .vehicle import Vehicle
from .parking_spot import ParkingSpot

class ParkingStrategy(ABC):
    @abstractmethod
    def find_parking_spot(
        self,
        floors: List[ParkingFloor],
        vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        pass

class NearestParkingStrategy(ParkingStrategy):
    def find_parking_spot(
        self,
        floors: List[ParkingFloor],
        vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        for floor in floors:
            for spot in floor.get_parking_spots():
                if spot.can_park_vehicle(vehicle):
                    return spot
        return None

class FarthestParkingStrategy(ParkingStrategy):
    def find_parking_spot(
        self,
        floors: List[ParkingFloor],
        vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        for floor in reversed(floors):
            for spot in reversed(floor.get_parking_spots()):
                if spot.can_park_vehicle(vehicle):
                    return spot
        return None

class BestFitParkingStrategy(ParkingStrategy):
    def find_parking_spot(
        self,
        floors: List[ParkingFloor],
        vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        best_spot = None
        for floor in floors:
            for spot in floor.get_parking_spots():
                if spot.can_park_vehicle(vehicle):
                    if best_spot is None or self._is_better_fit(spot, best_spot, vehicle):
                        best_spot = spot
        return best_spot

    def _is_better_fit(self, spot1: ParkingSpot, spot2: ParkingSpot, vehicle: Vehicle) -> bool:
        # Implement logic to determine which spot is a better fit for the vehicle
        # For example, you can compare the sizes of the spots and the vehicle
        return spot1.get_type().value < spot2.get_type().value