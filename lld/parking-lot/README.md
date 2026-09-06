# Designing a Parking Lot System

## Requirements

1. System supports different vehicle types such as motorcycle, car, and truck.
2. System supports multiple floors with different parking spots.
3. System automatically assigns an available compatible spot when a vehicle enters.
4. System issues a ticket at entry.
5. When a vehicle exits, the user provides the ticket ID:
   - System validates the ticket.
   - Calculates the fee based on parking duration and vehicle type.
   - Frees the parking spot for the next vehicle.
6. System rejects entry if no compatible parking spot is available.
7. System rejects exit if the ticket is invalid or has already been used.

## Out of Scope

- Payment processing
- Advance reservations

## Core Entities

- **Vehicle** - Represents a vehicle entering the parking lot. It contains the registration number and vehicle type.
- **ParkingSpot** - Represents a physical parking spot. It has an ID, spot type, and state, and keeps track of the vehicle currently parked in it.
- **ParkingFloor** - Contains all parking spots on a floor.
- **ParkingLot** - Acts as the main orchestrator. It manages floors, active tickets, parking allocation, and fee calculation.
- **VehicleType** - Enum defining the supported vehicle types.
- **SpotType** - Enum defining the physical sizes of parking spots.
- **Ticket** - Represents a parking session. It contains the ticket ID, vehicle, assigned parking spot, entry time, exit time, and status.
- **SpotState** - Enum defining the possible states of a parking spot.
- **TicketStatus** - Enum defining the lifecycle of a parking ticket.
- **ParkingStrategy** - Defines how the system selects an available parking spot.
- **FeeStrategy** - Defines how the parking fee is calculated.

## Class Design
```mermaid
class Vehicle {
    -String regnNo
    -VehicleType type
    +Vehicle(String regnNo, VehicleType type)
    +getRegnNo() String
    +getType() VehicleType
}

class ParkingSpot {
    -String id
    -SpotState state
    -SpotType type
    -Vehicle parkedVehicle
    +ParkingSpot(String id, SpotType type)
    +getId() String
    +getType() SpotType
    +getState() SpotState
    +isAvailable() Boolean
    +isOccupied() Boolean
    +parkVehicle(Vehicle vehicle)
    +freeSpot()
    +canParkVehicle(Vehicle vehicle) Boolean
}

class ParkingFloor {
    -List<ParkingSpot> parkingSpots
    +ParkingFloor(List<ParkingSpot> parkingSpots)
    +getParkingSpots() List<ParkingSpot>
}

class ParkingLot {
    -List<ParkingFloor> floors
    -Map<String, Ticket> activeTickets
    -FeeStrategy feeStrategy
    -ParkingStrategy parkingStrategy
    +addFloor(ParkingFloor floor)
    +setFeeStrategy(FeeStrategy strategy)
    +setParkingStrategy(ParkingStrategy strategy)
    +enter(Vehicle vehicle) Ticket
    +exit(String ticketId) double
}

class Ticket {
    -String id
    -ParkingSpot spot
    -Vehicle vehicle
    -long entryTime
    -long exitTime
    -TicketStatus status
    +Ticket(String id, ParkingSpot spot, Vehicle vehicle, long entryTime)
    +getId() String
    +getStatus() TicketStatus
    +getEntryTime() long
    +getExitTime() long
    +getVehicle() Vehicle
    +getSpot() ParkingSpot
    +complete(long exitTime)
}

class ParkingStrategy {
    +findSpot(List~ParkingFloor~ floors, Vehicle vehicle) ParkingSpot
}

class FeeStrategy {
    +calculateFee(Ticket ticket, long exitTime) double
}

enum VehicleType {
    MOTORCYCLE
    CAR
    TRUCK
}

enum SpotType {
    SMALL
    MEDIUM
    LARGE
}

enum SpotState {
    AVAILABLE
    OCCUPIED
    OUT_OF_SERVICE
}

enum TicketStatus {
    ACTIVE
    COMPLETED
}
```