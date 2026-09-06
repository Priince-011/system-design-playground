from .parking_spot import ParkingSpot

class ParkingFloor:
    def __init__(self, floor_id: str):
        self.id = floor_id
        self.parking_spots = []
    
    def add_parking_spot(self, parking_spot: ParkingSpot):
        self.parking_spots.append(parking_spot)
    
    def get_parking_spots(self) -> list[ParkingSpot]:
        return self.parking_spots