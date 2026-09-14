import uuid
import time
from .vehicle import Vehicle
from .parking_spot import ParkingSpot
from .ticket_status import TicketStatus


class Ticket:
    """Represents a parking session.
    
    Tracks:
    - Ticket ID
    - Vehicle and spot
    - Entry/exit times
    - Status (ACTIVE -> PAID -> CLOSED)
    """
    
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot):
        self.id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.entry_time = int(time.time() * 1000)  # milliseconds
        self.exit_time = None
        self.status = TicketStatus.ACTIVE

    def get_id(self) -> str:
        return self.id
    
    def get_status(self) -> TicketStatus:
        return self.status
    
    def get_vehicle(self) -> Vehicle:
        return self.vehicle
    
    def get_parking_spot(self) -> ParkingSpot:
        return self.parking_spot
    
    def get_entry_time(self) -> int:
        """Get entry time in milliseconds."""
        return self.entry_time
    
    def get_exit_time(self) -> int:
        """Get exit time in milliseconds."""
        if self.exit_time is None:
            raise ValueError("Exit time not set for active ticket")
        return self.exit_time
    
    def mark_exit(self) -> None:
        """Mark vehicle as exited and transition to PAID.
        
        Raises:
            ValueError: If ticket is not ACTIVE.
        """
        if self.status != TicketStatus.ACTIVE:
            raise ValueError(f"Cannot exit ticket in state {self.status}")
        self.exit_time = int(time.time() * 1000)
        self.status = TicketStatus.PAID
    
    def close(self) -> None:
        """Close the ticket after payment.
        
        Raises:
            ValueError: If ticket is not PAID.
        """
        if self.status != TicketStatus.PAID:
            raise ValueError(f"Can only close PAID tickets, current status: {self.status}")
        self.status = TicketStatus.CLOSED
