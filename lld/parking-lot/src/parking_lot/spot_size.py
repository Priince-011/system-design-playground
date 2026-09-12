from enum import Enum


class SpotSize(Enum):
    """Parking spot size levels.
    
    Size hierarchy: SMALL < MEDIUM < LARGE
    
    A MEDIUM vehicle can use MEDIUM or LARGE spots.
    A MEDIUM spot can accommodate SMALL or MEDIUM vehicles.
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    
    def can_fit_vehicle_size(self, vehicle_size: 'VehicleSize') -> bool:
        """Check if this spot size can fit a vehicle of the given size."""
        # Import here to avoid circular dependency
        from .vehicle_size import VehicleSize
        
        # Map VehicleSize to SpotSize for comparison
        vehicle_spot_size = SpotSize[vehicle_size.name]
        return self.value >= vehicle_spot_size.value
