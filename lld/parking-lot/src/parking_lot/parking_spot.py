from .spot_size import SpotSize
from .spot_state import SpotState
from .vehicle import Vehicle


class ParkingSpot:
    """Represents a physical parking spot.
    
    Responsibilities:
    - Manage own state (AVAILABLE, OCCUPIED, OUT_OF_SERVICE)
    - Determine if a vehicle can fit based on size
    - Park/remove vehicles while enforcing invariants
    - Prevent invalid state transitions
    """
    
    def __init__(self, spot_id: str, size: SpotSize):
        self.id = spot_id
        self.size = size
        self.state = SpotState.AVAILABLE
        self.parked_vehicle = None

    def get_id(self) -> str:
        return self.id
    
    def get_size(self) -> SpotSize:
        return self.size
    
    def get_state(self) -> SpotState:
        return self.state
    
    def is_available(self) -> bool:
        return self.state == SpotState.AVAILABLE
    
    def is_occupied(self) -> bool:
        return self.state == SpotState.OCCUPIED
    
    def is_out_of_service(self) -> bool:
        return self.state == SpotState.OUT_OF_SERVICE
    
    def can_fit(self, vehicle: Vehicle) -> bool:
        """Check if this spot can accommodate a vehicle.
        
        Spot must be:
        1. Available
        2. Not out of service
        3. Large enough for the vehicle
        """
        if not self.is_available():
            return False
        if self.is_out_of_service():
            return False
        return self.size.can_fit_vehicle_size(vehicle.get_size())
    
    def park(self, vehicle: Vehicle) -> None:
        """Park a vehicle in this spot.
        
        Raises:
            ValueError: If spot is not available, out of service, or vehicle doesn't fit.
        """
        if not self.is_available():
            raise ValueError(f"Spot {self.id} is not available (state: {self.state})")
        if self.is_out_of_service():
            raise ValueError(f"Spot {self.id} is out of service")
        if not self.can_fit(vehicle):
            raise ValueError(
                f"Vehicle {vehicle.get_registration_number()} "
                f"(size: {vehicle.get_size().name}) "
                f"does not fit in {self.id} (size: {self.size.name})"
            )
        
        self.state = SpotState.OCCUPIED
        self.parked_vehicle = vehicle
    
    def remove_vehicle(self) -> Vehicle:
        """Remove the parked vehicle and free the spot.
        
        Returns:
            The vehicle that was parked.
            
        Raises:
            ValueError: If no vehicle is parked.
        """
        if self.parked_vehicle is None:
            raise ValueError(f"Spot {self.id} is empty")
        
        vehicle = self.parked_vehicle
        self.state = SpotState.AVAILABLE
        self.parked_vehicle = None
        return vehicle
    
    def mark_out_of_service(self) -> None:
        """Mark this spot as out of service (maintenance, etc.)."""
        self.state = SpotState.OUT_OF_SERVICE
        self.parked_vehicle = None
    
    def restore_to_service(self) -> None:
        """Restore this spot to service."""
        self.state = SpotState.AVAILABLE
