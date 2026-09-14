"""Tests for ParkingSpot functionality."""
import pytest
from src.parking_lot.parking_spot import ParkingSpot
from src.parking_lot.spot_size import SpotSize
from src.parking_lot.spot_state import SpotState
from src.parking_lot.motorcycle import Motorcycle
from src.parking_lot.car import Car
from src.parking_lot.truck import Truck
from src.parking_lot.vehicle_size import VehicleSize


class TestParkingSpotFitness:
    """Test vehicle-spot compatibility based on size."""
    
    def test_small_vehicle_fits_in_small_spot(self):
        spot = ParkingSpot("S1", SpotSize.SMALL)
        motorcycle = Motorcycle("MOTO-001", VehicleSize.SMALL)
        assert spot.can_fit(motorcycle)
    
    def test_small_vehicle_fits_in_medium_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        motorcycle = Motorcycle("MOTO-001", VehicleSize.SMALL)
        assert spot.can_fit(motorcycle)
    
    def test_small_vehicle_fits_in_large_spot(self):
        spot = ParkingSpot("L1", SpotSize.LARGE)
        motorcycle = Motorcycle("MOTO-001", VehicleSize.SMALL)
        assert spot.can_fit(motorcycle)
    
    def test_medium_vehicle_fits_in_medium_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001", VehicleSize.MEDIUM)
        assert spot.can_fit(car)
    
    def test_medium_vehicle_fits_in_large_spot(self):
        spot = ParkingSpot("L1", SpotSize.LARGE)
        car = Car("CAR-001", VehicleSize.MEDIUM)
        assert spot.can_fit(car)
    
    def test_medium_vehicle_does_not_fit_in_small_spot(self):
        spot = ParkingSpot("S1", SpotSize.SMALL)
        car = Car("CAR-001", VehicleSize.MEDIUM)
        assert not spot.can_fit(car)
    
    def test_large_vehicle_fits_in_large_spot(self):
        spot = ParkingSpot("L1", SpotSize.LARGE)
        truck = Truck("TRUCK-001", VehicleSize.LARGE)
        assert spot.can_fit(truck)
    
    def test_large_vehicle_does_not_fit_in_small_spot(self):
        spot = ParkingSpot("S1", SpotSize.SMALL)
        truck = Truck("TRUCK-001", VehicleSize.LARGE)
        assert not spot.can_fit(truck)
    
    def test_large_vehicle_does_not_fit_in_medium_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        truck = Truck("TRUCK-001", VehicleSize.LARGE)
        assert not spot.can_fit(truck)


class TestParkingSpotParking:
    """Test parking and removal operations."""
    
    def test_park_vehicle_in_available_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        spot.park(car)
        assert spot.is_occupied()
        assert spot.parked_vehicle == car
    
    def test_cannot_park_in_occupied_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car1 = Car("CAR-001")
        car2 = Car("CAR-002")
        spot.park(car1)
        
        with pytest.raises(ValueError, match="not available"):
            spot.park(car2)
    
    def test_cannot_park_incompatible_vehicle(self):
        spot = ParkingSpot("S1", SpotSize.SMALL)
        car = Car("CAR-001", VehicleSize.MEDIUM)
        
        with pytest.raises(ValueError, match="does not fit"):
            spot.park(car)
    
    def test_cannot_park_in_out_of_service_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        spot.mark_out_of_service()
        car = Car("CAR-001")
        
        with pytest.raises(ValueError, match="out of service"):
            spot.park(car)
    
    def test_remove_vehicle_frees_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        car = Car("CAR-001")
        spot.park(car)
        
        removed = spot.remove_vehicle()
        assert removed == car
        assert spot.is_available()
        assert spot.parked_vehicle is None
    
    def test_cannot_remove_from_empty_spot(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        with pytest.raises(ValueError, match="empty"):
            spot.remove_vehicle()
    
    def test_mark_out_of_service(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        spot.mark_out_of_service()
        assert spot.is_out_of_service()
    
    def test_restore_to_service(self):
        spot = ParkingSpot("M1", SpotSize.MEDIUM)
        spot.mark_out_of_service()
        spot.restore_to_service()
        assert spot.is_available()
