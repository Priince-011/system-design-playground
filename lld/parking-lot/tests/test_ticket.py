"""Tests for Ticket functionality."""
import pytest
from src.parking_lot.ticket import Ticket
from src.parking_lot.ticket_status import TicketStatus
from src.parking_lot.parking_spot import ParkingSpot
from src.parking_lot.spot_size import SpotSize
from src.parking_lot.car import Car


class TestTicketLifecycle:
    """Test ticket state transitions."""
    
    def test_ticket_starts_active(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        ticket = Ticket(car, spot)
        
        assert ticket.get_status() == TicketStatus.ACTIVE
    
    def test_mark_exit_transitions_to_paid(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        ticket = Ticket(car, spot)
        
        ticket.mark_exit()
        assert ticket.get_status() == TicketStatus.PAID
    
    def test_close_transitions_to_closed(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        ticket = Ticket(car, spot)
        
        ticket.mark_exit()
        ticket.close()
        assert ticket.get_status() == TicketStatus.CLOSED
    
    def test_cannot_mark_exit_twice(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        ticket = Ticket(car, spot)
        
        ticket.mark_exit()
        with pytest.raises(ValueError, match="not ACTIVE"):
            ticket.mark_exit()
    
    def test_cannot_close_active_ticket(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        ticket = Ticket(car, spot)
        
        with pytest.raises(ValueError, match="only close PAID"):
            ticket.close()
    
    def test_get_exit_time_fails_for_active_ticket(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        ticket = Ticket(car, spot)
        
        with pytest.raises(ValueError, match="Exit time not set"):
            ticket.get_exit_time()
