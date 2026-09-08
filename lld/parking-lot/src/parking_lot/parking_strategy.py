from abc import ABC, abstractmethod
from typing import List, Optional
from .parking_floor import ParkingFloor
from .vehicle import Vehicle
from .parking_spot import ParkingSpot
from .spot_type import SpotType

class ParkingStrategy(ABC):
    @abstractmethod
    def find_parking_spot(
        self,
        floors: List[ParkingFloor],
        vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        pass

class FirstAvailableParkingStrategy(ParkingStrategy):
    """Returns the first available compatible spot."""
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
    """Returns the farthest available compatible spot (last floor, last spot)."""
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
    """Returns the smallest compatible spot that fits the vehicle (best fit)."""
    
    # Map SpotType to numeric size for proper ordering
    SPOT_SIZE_PRIORITY = {
        SpotType.SMALL: 1,
        SpotType.MEDIUM: 2,
        SpotType.LARGE: 3
    }
    
    def find_parking_spot(
        self,
        floors: List[ParkingFloor],
        vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        best_spot = None
        for floor in floors:
            for spot in floor.get_parking_spots():
                if spot.can_park_vehicle(vehicle):
                    if best_spot is None or self._is_better_fit(spot, best_spot):
                        best_spot = spot
        return best_spot

    def _is_better_fit(self, spot1: ParkingSpot, spot2: ParkingSpot) -> bool:
        """Compare spots by size: prefer smaller spots (best fit algorithm)."""
        size1 = self.SPOT_SIZE_PRIORITY.get(spot1.get_type(), 999)
        size2 = self.SPOT_SIZE_PRIORITY.get(spot2.get_type(), 999)
        return size1 < size2
