from abc import ABC, abstractmethod
from .ticket import Ticket


class ParkingFeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        pass

class FixedParkingFeeStrategy(ParkingFeeStrategy):
    def __init__(self, fixed_fee: float):
        self.fixed_fee = fixed_fee

    def calculate_fee(self, ticket: Ticket) -> float:
        return self.fixed_fee
    
class FlatHourlyParkingFeeStrategy(ParkingFeeStrategy):
    def __init__(self, hourly_rate: float):
        self.hourly_rate = hourly_rate

    def calculate_fee(self, ticket: Ticket) -> float:
        if ticket.get_exit_time() is None:
            raise ValueError("Exit time is not set for the ticket.")
        
        duration_in_millis = ticket.get_exit_time() - ticket.get_entry_time()
        duration_in_hours = duration_in_millis / (1000 * 60 * 60)
        return self.hourly_rate * duration_in_hours
    
class VehicleBasedHourlyParkingFeeStrategy(ParkingFeeStrategy):
    def __init__(self, hourly_rates: dict):
        self.hourly_rates = hourly_rates

    def calculate_fee(self, ticket: Ticket) -> float:
        duration = ticket.get_exit_time() - ticket.get_entry_time()
        hours = (duration // (1000 * 60 * 60)) + 1
        return hours * self.hourly_rates[ticket.get_vehicle().get_size()]