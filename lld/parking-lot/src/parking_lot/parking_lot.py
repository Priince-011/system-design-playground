import uuid
from typing import Dict, List, Optional
from .parking_floor import ParkingFloor
from .vehicle import Vehicle
from .ticket import Ticket
from .parking_strategy import ParkingStrategy
from .parking_fee_strategy import ParkingFeeStrategy

class ParkingLot:
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
        self.active_tickets: Dict[str, Ticket] = {}  # Maps ticket ID to Ticket Object
    
    def add_parking_floor(self, parking_floor: ParkingFloor):
        self.floors.append(parking_floor)
    
    def set_parking_strategy(self, parking_strategy: ParkingStrategy):
        self.parking_strategy = parking_strategy

    def set_parking_fee_strategy(self, parking_fee_strategy: ParkingFeeStrategy):
        self.parking_fee_strategy = parking_fee_strategy
    
    def enter(self, vehicle: Vehicle) -> Optional[Ticket]:
        """Allow vehicle to enter and park in an available compatible spot."""
        parking_spot = self.parking_strategy.find_parking_spot(self.floors, vehicle)
        if parking_spot:
            try:
                parking_spot.park_vehicle(vehicle)
                ticket = Ticket(vehicle, parking_spot)
                self.active_tickets[ticket.get_id()] = ticket
                return ticket
            except ValueError as e:
                print(f"Failed to park vehicle: {e}")
                return None
        else:
            print("No available parking spot for the vehicle.")
            return None
    
    def exit(self, ticket_id: str) -> Optional[float]:
        """Allow vehicle to exit by ticket ID."""
        ticket = self.active_tickets.get(ticket_id)
        if ticket:
            try:
                ticket.set_exit_timestamp()
                parking_spot = ticket.get_parking_spot()
                parking_spot.free_parking_spot()
                fee = self.parking_fee_strategy.calculate_fee(ticket)
                del self.active_tickets[ticket_id]
                return fee
            except ValueError as e:
                print(f"Failed to process exit: {e}")
                return None
        else:
            print("Invalid ticket ID.")
            return None
