import uuid
from typing import Dict, List, Optional
from .parking_floor import ParkingFloor
from .vehicle import Vehicle
from .ticket import Ticket
from .parking_strategy import ParkingStrategy
from .parking_fee_strategy import ParkingFeeStrategy


class ParkingLot:
    """Main orchestrator for parking operations.
    
    Responsibilities:
    - Manage parking floors and spots
    - Coordinate vehicle entry/exit
    - Delegate spot selection to ParkingStrategy
    - Delegate fee calculation to ParkingFeeStrategy
    - Maintain active tickets
    """
    
    def __init__(
        self,
        name: str,
        floors: List[ParkingFloor],
        parking_strategy: ParkingStrategy,
        parking_fee_strategy: ParkingFeeStrategy
    ):
        self.name = name
        self.id = str(uuid.uuid4())
        self.floors = floors
        self.parking_strategy = parking_strategy
        self.parking_fee_strategy = parking_fee_strategy
        self.active_tickets: Dict[str, Ticket] = {}
    
    def add_floor(self, floor: ParkingFloor) -> None:
        self.floors.append(floor)
    
    def set_parking_strategy(self, strategy: ParkingStrategy) -> None:
        self.parking_strategy = strategy
    
    def set_parking_fee_strategy(self, strategy: ParkingFeeStrategy) -> None:
        self.parking_fee_strategy = strategy
    
    def enter(self, vehicle: Vehicle) -> Optional[Ticket]:
        """Process vehicle entry.
        
        Returns:
            Ticket if spot found and parked successfully, None otherwise.
        """
        spot = self.parking_strategy.find_spot(self.floors, vehicle)
        
        if not spot:
            return None
        
        try:
            spot.park(vehicle)
            ticket = Ticket(vehicle, spot)
            self.active_tickets[ticket.get_id()] = ticket
            return ticket
        except ValueError:
            return None
    
    def exit(self, ticket_id: str) -> Optional[float]:
        """Process vehicle exit and calculate fee.
        
        Args:
            ticket_id: The parking ticket ID
            
        Returns:
            Calculated fee if exit successful, None otherwise.
        """
        ticket = self.active_tickets.get(ticket_id)
        
        if not ticket:
            return None
        
        try:
            ticket.mark_exit()
            spot = ticket.get_parking_spot()
            spot.remove_vehicle()
            
            fee = self.parking_fee_strategy.calculate_fee(ticket)
            ticket.close()
            
            del self.active_tickets[ticket_id]
            return fee
        except ValueError:
            return None
    
    def get_available_spots(self) -> int:
        """Count total available spots across all floors."""
        count = 0
        for floor in self.floors:
            for spot in floor.get_parking_spots():
                if spot.is_available():
                    count += 1
        return count
    
    def get_occupied_spots(self) -> int:
        """Count total occupied spots across all floors."""
        count = 0
        for floor in self.floors:
            for spot in floor.get_parking_spots():
                if spot.is_occupied():
                    count += 1
        return count
