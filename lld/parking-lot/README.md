# Designing a Parking Lot System

## Requirements
1. System supports different vehicle sizes like motorcycle, car, and trucks.
2. System supports mutiple floors having different parking spots.
3. System automatically assigns a available compatible spot when a vehicle enters.
4. System issues a ticket at entry.
5. When vehicle exits, User provides ticket id
    - System validates the tickets
    - Calculates the fee based on hourly rate and type of vehicle
    - Frees the spot for next use
6. System rejects entry if no compatible spot available
7. System rejects exit if ticket is invalid or already used

## Out of scope
- Payment procesing
- Advance reservation


## Core entities
- **Vehicle** - This can be an abstract class, which can be extented by Car, Motorcycle and Truck classes.
- **ParkingSpot** - This represents a physical spot. It has an ID, a type to match with vehicle type, a state to track availability/occupancy.
- **ParkingFloor** - This contains all the parking spots on that floor.
- **ParkingLot** - This is the entry point to the system. When a vehicle enters, it will look for the avaible parking spot, generate parking ticket and mark the spot occupied. When a vehicle exits it will validate the ticket, calculate the parking fee and free the spot.
- **VehicleType** - This is an enum that define the supported vehicle types in parking lot.
- **Ticket** - When a available parking spot is assigned to a vehicle, the system generates a ticket, it hold the ticket id, occupied spot, vehicle, entry time, status.
- **SpotState** - This is an enum that defines the possible states of the parking spot.



## Class Design
```mermaid
class Vehicle:
    - regnNo: String
    - type: VehicleType

    + Vehicle(regnNo, type)
    + getRegnNo() -> String
    + getType() -> VehicleType
```
```
class ParkingSpot:
    - id: String
    - state: SpotState
    - type: SpotType
    - parkedVehicle: Vehicle

    + ParkingSpot(id, type)
    + getId() -> String
    + getType() -> SpotType
    + getState() -> SpotState
    + isAvailable() -> Boolean
    + isOccupied() -> Boolean
    + parkVehicle(vehicle)
    + freeSpot()
    + canParkVehicle(vehicle) -> Boolean
```
```
class ParkingFloor:
    - parkingSpots: list<ParkingSpot>

    + ParkingFloor(parkingSpots)
    + getParkingSpots() -> list<ParkingSpot>
```
```
class ParkingLot:
    - floors: list<ParkingFloor>
    - activeTickets: map<string, Ticket>
    - feeStrategy: FeeStrategy
    - parkingStrategy: parkingStrategy

    + addFloor()
    + setFeeStrategy()
    + setParkingStartegy()
    + enter()
    + exit()
    
```
```
enum VehicleType:
    - MOTORCYCLE
    - CAR
    - TRUCK
```
```
enum SpotType:
    - SMALL
    - MEDIUM
    - LARGE
```
```
class Ticket:
    - id: String
    - spot: ParkingSpot
    - vehicle: Vehicle
    - entryTime: long
    - status: TicketStatus
    
    + Ticket(id, spotId, vehicle, entryTime)
    + getStatus()
    + getEntryTime()
    + getVehicle()
    + getId()
```
```
enum SpotState:
    - AVAILABLE
    - OCCUPIED
    - NOTAVAILABLE
```
```
enum TicketStatus:
    - ACTIVE
    - EXPIRED
```
