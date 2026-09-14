"""Integration tests for parking lot enter/exit flows."""
import pytest
from src.parking_lot.parking_lot import ParkingLot
from src.parking_lot.parking_floor import ParkingFloor
from src.parking_lot.parking_spot import ParkingSpot
from src.parking_lot.spot_size import SpotSize
from src.parking_lot.parking_strategy import BestFitStrategy
from src.parking_lot.parking_fee_strategy import HourlyFeeStrategy
from src.parking_lot.car import Car
from src.parking_lot.motorcycle import Motorcycle
from src.parking_lot.truck import Truck
from src.parking_lot.vehicle_size import VehicleSize


class TestParkingLotEntry:
    """Test vehicle entry to parking lot."""
    
    def test_vehicle_enters_and_gets_ticket(self):
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        
        lot = ParkingLot(
            "TestLot",
            [floor],
            BestFitStrategy(),
            HourlyFeeStrategy(10.0)
        )
        
        car = Car("CAR-001")
        ticket = lot.enter(car)
        
        assert ticket is not None
        assert ticket.get_vehicle() == car
        assert ticket.get_parking_spot().is_occupied()
    
    def test_entry_fails_when_no_spot_available(self):
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
        
        lot = ParkingLot(
            "TestLot",
            [floor],
            BestFitStrategy(),
            HourlyFeeStrategy(10.0)
        )
        
        truck = Truck("TRUCK-001", VehicleSize.LARGE)
        ticket = lot.enter(truck)
        
        assert ticket is None
    
    def test_multiple_vehicles_park_in_different_spots(self):
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
        floor.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        
        lot = ParkingLot(
            "TestLot",
            [floor],
            BestFitStrategy(),
            HourlyFeeStrategy(10.0)
        )
        
        moto = Motorcycle("MOTO-001")
        car = Car("CAR-001")
        
        ticket1 = lot.enter(moto)
        ticket2 = lot.enter(car)
        
        assert ticket1 is not None
        assert ticket2 is not None
        assert ticket1.get_parking_spot() != ticket2.get_parking_spot()


class TestParkingLotExit:
    """Test vehicle exit from parking lot."""
    
    def test_vehicle_exits_and_spot_freed(self):
        floor = ParkingFloor("F1")
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        floor.add_parking_spot(spot)
        
        lot = ParkingLot(
            "TestLot",
            [floor],
            BestFitStrategy(),
            HourlyFeeStrategy(10.0)
        )
        
        car = Car("CAR-001")
        ticket = lot.enter(car)
        assert spot.is_occupied()
        
        fee = lot.exit(ticket.get_id())
        assert fee is not None
        assert spot.is_available()
    
    def test_exit_with_invalid_ticket_returns_none(self):
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        
        lot = ParkingLot(
            "TestLot",
            [floor],
            BestFitStrategy(),
            HourlyFeeStrategy(10.0)
        )
        
        fee = lot.exit("invalid-ticket-id")
        assert fee is None


class TestParkingLotFullScenario:
    """Full parking lot operations scenario."""
    
    def test_full_parking_flow(self):
        # Setup: 2 floors, mixed spot sizes
        floor1 = ParkingFloor("F1")
        floor1.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
        floor1.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        
        floor2 = ParkingFloor("F2")
        floor2.add_parking_spot(ParkingSpot("L1", SpotSize.LARGE))
        
        lot = ParkingLot(
            "MegaLot",
            [floor1, floor2],
            BestFitStrategy(),
            HourlyFeeStrategy(10.0)
        )
        
        # Motorcycle parks in S1
        moto = Motorcycle("MOTO-001")
        moto_ticket = lot.enter(moto)
        assert moto_ticket is not None
        assert lot.get_occupied_spots() == 1
        
        # Car parks in M1
        car = Car("CAR-001")
        car_ticket = lot.enter(car)
        assert car_ticket is not None
        assert lot.get_occupied_spots() == 2
        
        # Truck parks in L1
        truck = Truck("TRUCK-001")
        truck_ticket = lot.enter(truck)
        assert truck_ticket is not None
        assert lot.get_occupied_spots() == 3
        assert lot.get_available_spots() == 0
        
        # Motorcycle exits
        moto_fee = lot.exit(moto_ticket.get_id())
        assert moto_fee is not None
        assert lot.get_occupied_spots() == 2
        assert lot.get_available_spots() == 1
