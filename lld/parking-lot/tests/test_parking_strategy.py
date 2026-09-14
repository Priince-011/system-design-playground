"""Tests for parking spot selection strategies."""
import pytest
from src.parking_lot.parking_strategy import (
    FirstAvailableStrategy,
    BestFitStrategy,
    FarthestParkingStrategy
)
from src.parking_lot.parking_floor import ParkingFloor
from src.parking_lot.parking_spot import ParkingSpot
from src.parking_lot.spot_size import SpotSize
from src.parking_lot.car import Car
from src.parking_lot.motorcycle import Motorcycle
from src.parking_lot.truck import Truck
from src.parking_lot.vehicle_size import VehicleSize


class TestFirstAvailableStrategy:
    """Test first-available spot selection."""
    
    def test_finds_first_available_spot(self):
        strategy = FirstAvailableStrategy()
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
        floor.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        
        car = Car("CAR-001", VehicleSize.MEDIUM)
        spot = strategy.find_spot([floor], car)
        
        assert spot is not None
        assert spot.get_id() == "M1"
    
    def test_returns_none_when_no_spot_available(self):
        strategy = FirstAvailableStrategy()
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
        
        truck = Truck("TRUCK-001", VehicleSize.LARGE)
        spot = strategy.find_spot([floor], truck)
        
        assert spot is None


class TestBestFitStrategy:
    """Test best-fit (smallest compatible) spot selection."""
    
    def test_selects_smallest_compatible_spot(self):
        """MEDIUM vehicle should select MEDIUM spot, not LARGE."""
        strategy = BestFitStrategy()
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        floor.add_parking_spot(ParkingSpot("L1", SpotSize.LARGE))
        floor.add_parking_spot(ParkingSpot("L2", SpotSize.LARGE))
        
        car = Car("CAR-001", VehicleSize.MEDIUM)
        spot = strategy.find_spot([floor], car)
        
        assert spot is not None
        assert spot.get_id() == "M1"
        assert spot.get_size() == SpotSize.MEDIUM
    
    def test_fits_in_smallest_available(self):
        """When best size not available, select next larger."""
        strategy = BestFitStrategy()
        floor = ParkingFloor("F1")
        floor.add_parking_spot(ParkingSpot("L1", SpotSize.LARGE))
        
        car = Car("CAR-001", VehicleSize.MEDIUM)
        spot = strategy.find_spot([floor], car)
        
        assert spot is not None
        assert spot.get_size() == SpotSize.LARGE


class TestFarthestParkingStrategy:
    """Test farthest spot selection (last floor, last spot)."""
    
    def test_selects_last_floor_last_spot(self):
        strategy = FarthestParkingStrategy()
        
        floor1 = ParkingFloor("F1")
        floor1.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
        floor1.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))
        
        floor2 = ParkingFloor("F2")
        floor2.add_parking_spot(ParkingSpot("S2", SpotSize.SMALL))
        floor2.add_parking_spot(ParkingSpot("M2", SpotSize.MEDIUM))
        
        car = Car("CAR-001", VehicleSize.MEDIUM)
        spot = strategy.find_spot([floor1, floor2], car)
        
        assert spot is not None
        assert spot.get_id() == "M2"
