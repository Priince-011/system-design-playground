from abc import ABC, abstractmethod
from .ticket import Ticket
from .vehicle_type import VehicleType


class ParkingFeeStrategy(ABC):
    """Strategy for calculating parking fees."""
    
    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        pass


class FixedFeeStrategy(ParkingFeeStrategy):
    """Flat fee regardless of duration."""
    
    def __init__(self, fee: float):
        self.fee = fee
    
    def calculate_fee(self, ticket: Ticket) -> float:
        return self.fee


class HourlyFeeStrategy(ParkingFeeStrategy):
    """Hourly rate, same for all vehicle types."""
    
    def __init__(self, hourly_rate: float):
        self.hourly_rate = hourly_rate
    
    def calculate_fee(self, ticket: Ticket) -> float:
        duration_ms = ticket.get_exit_time() - ticket.get_entry_time()
        hours = max(1, duration_ms / (1000 * 60 * 60))  # round up to 1 hour minimum
        return self.hourly_rate * hours


class VehicleTypeHourlyFeeStrategy(ParkingFeeStrategy):
    """Hourly rate varies by vehicle type."""
    
    def __init__(self, hourly_rates: dict):
        """hourly_rates: {VehicleType: rate_float}"""
        self.hourly_rates = hourly_rates
    
    def calculate_fee(self, ticket: Ticket) -> float:
        vehicle_type = ticket.get_vehicle().get_vehicle_type()
        if vehicle_type not in self.hourly_rates:
            raise ValueError(f"No rate defined for vehicle type {vehicle_type}")
        
        rate = self.hourly_rates[vehicle_type]
        duration_ms = ticket.get_exit_time() - ticket.get_entry_time()
        hours = max(1, duration_ms / (1000 * 60 * 60))
        return rate * hours
