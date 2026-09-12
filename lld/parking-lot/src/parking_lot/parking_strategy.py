from abc import ABC, abstractmethod
from typing import List, Optional
from .parking_floor import ParkingFloor
from .vehicle import Vehicle
from .parking_spot import ParkingSpot
from .spot_size import SpotSize


class ParkingStrategy(ABC):
    """Abstract strategy for selecting a parking spot."""
    
    @abstractmethod
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        pass


class FirstAvailableStrategy(ParkingStrategy):
    """Returns the first available spot that fits the vehicle."""
    
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in floors:
            for spot in floor.get_parking_spots():
                if spot.can_fit(vehicle):
                    return spot
        return None


class BestFitStrategy(ParkingStrategy):
    """Returns the smallest available spot that fits the vehicle.
    
    Example:
    - Vehicle size: MEDIUM
    - Available spots: SMALL, MEDIUM, LARGE
    - Result: MEDIUM (best fit)
    """
    
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        best_spot = None
        for floor in floors:
            for spot in floor.get_parking_spots():
                if spot.can_fit(vehicle):
                    if best_spot is None or self._is_better_fit(spot, best_spot):
                        best_spot = spot
        return best_spot
    
    def _is_better_fit(self, spot1: ParkingSpot, spot2: ParkingSpot) -> bool:
        """Compare spots: prefer smaller size."""
        return spot1.get_size().value < spot2.get_size().value


class FarthestParkingStrategy(ParkingStrategy):
    """Returns the farthest available spot (last floor, last spot)."""
    
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in reversed(floors):
            for spot in reversed(floor.get_parking_spots()):
                if spot.can_fit(vehicle):
                    return spot
        return None
