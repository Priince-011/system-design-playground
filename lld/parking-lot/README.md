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
8. System should be extensible to various parking and fee calculation strategies.

## Out of Scope

- Payment processing
- Advance reservations

## Core Components

### Domain Models

- **Vehicle** - Abstract base class representing a vehicle entering the parking lot. It contains information common to all vehicle types and defines common behavior and allows concrete vehicle types to provide type-specific behavior.

- **ParkingSpot** - Represents a physical parking spot. It has an ID, spot type, and state, and keeps track of the vehicle currently parked in it.

- **ParkingFloor** - Represents a parking floor and contains all parking spots on that floor.

- **ParkingLot** - Acts as the main orchestrator. It manages floors, active tickets, parking allocation, and fee calculation.

- **Ticket** - Represents a parking session. It contains the ticket ID, vehicle, assigned parking spot, entry time, exit time, and status.

### Enums

- **SpotType** - Defines the physical sizes of parking spots.
- **SpotState** - Defines the possible states of a parking spot.
- **TicketStatus** - Defines the lifecycle states of a parking ticket.

### Strategies

- **ParkingStrategy** - Defines how the system selects an available parking spot.
- **FeeStrategy** - Defines how the parking fee is calculated.

## Class Design
### Vehicle

`Vehicle` is an abstract base class representing a vehicle entering the parking lot.

It contains the information common to all vehicle types:

- Registration number

The system supports the following concrete vehicle types:

- `Car`
- `Motorcycle`
- `Truck`

Each concrete vehicle type defines which parking spot types it is compatible with.

#### Why does it exist?

Using an abstract `Vehicle` allows common vehicle information and behavior to be defined once, while concrete vehicle types can provide type-specific behavior through polymorphism.

For example, `Car`, `Motorcycle`, and `Truck` may have different parking spot compatibility rules.

A vehicle is also a core domain object because multiple parts of the system need information about it:

- Parking allocation needs to determine whether the vehicle can fit in a parking spot.
- The ticket needs to identify the vehicle.
- Fee calculation may need information about the vehicle type.

### ParkingSpot
`ParkingSpot` represents a physical parking space in the parking lot.

It maintains:

- Spot ID
- Spot type
- Current state
- Vehicle currently parked in the spot

It is also responsible for managing its own occupancy state.

#### Key Behaviors

A parking spot should provide operations such as:

- Check whether it is available.
- Check whether a vehicle can be parked.
- Park a vehicle.
- Free the spot.

#### Why does ParkingSpot manage its own state?

The state of a parking spot should be controlled by the object that owns that state.

For example, instead of allowing `ParkingLot` to directly modify:

`spot.state = OCCUPIED`

the parking spot exposes:

`spot.parkVehicle(vehicle)`

This keeps the state transition inside `ParkingSpot` and allows the object to enforce its own invariants.

For example:

- A vehicle cannot be parked in an occupied spot.
- An incompatible vehicle cannot be parked in the spot.
- Freeing a spot removes the currently parked vehicle.

### ParkingFloor
`ParkingFloor` represents a single floor of the parking lot and contains the parking spots available on that floor.

Its primary responsibility is to group and provide access to the spots belonging to that floor.

#### Why does it exist?

A parking lot can contain multiple floors, and each floor contains multiple parking spots.

Instead of representing all spots as a flat collection inside `ParkingLot`, `ParkingFloor` models this hierarchy explicitly:

ParkingLot
→ ParkingFloor
→ ParkingSpot

This makes the domain model closer to the physical structure of the parking lot and allows parking strategies to reason about floors when selecting a spot.

### ParkingLot
`ParkingLot` acts as the main orchestrator for parking operations.

It coordinates:

- Parking floors
- Parking spot allocation
- Active tickets
- Fee calculation
- Vehicle entry
- Vehicle exit

It does not implement the parking allocation or fee calculation algorithms itself. Instead, it delegates these decisions to `ParkingStrategy` and `FeeStrategy`.

#### Why is ParkingLot an orchestrator?

A vehicle entering the parking lot requires multiple operations:

1. Find a compatible parking spot.
2. Occupy the spot.
3. Create a ticket.
4. Track the active ticket.

Similarly, vehicle exit requires:

1. Validate the ticket.
2. Calculate the fee.
3. Complete the ticket.
4. Free the parking spot.
5. Remove the ticket from active tickets.

`ParkingLot` coordinates these operations while delegating individual responsibilities to the appropriate components.

### Ticket
`Ticket` represents a single parking session.

It records:

- Ticket ID
- Vehicle
- Assigned parking spot
- Entry time
- Exit time
- Ticket status

#### Why is Ticket a separate domain object?

A vehicle and a parking session represent different concepts.

A `Vehicle` represents the physical vehicle, while a `Ticket` represents a particular visit to the parking lot.

The same vehicle may enter the parking lot multiple times, producing multiple tickets over its lifetime.

Therefore, parking-session information should not be stored directly inside `Vehicle`.

#### Ticket lifecycle

A ticket starts in the `ACTIVE` state.

When the vehicle exits:

`ACTIVE → COMPLETED`

The ticket records the exit time and can no longer be used for another exit operation.

### ParkingStrategy

`ParkingStrategy` Defines how the system selects an available compatible parking spot.

#### Why does it exist?

Parking spot selection can vary depending on the requirements.

For example:

- First available spot
- Nearest available spot
- Lowest-floor-first
- Spot selection based on specific preferences

Instead of embedding one selection algorithm inside `ParkingLot`, the strategy is separated behind an abstraction.

This allows the parking allocation policy to change without modifying `ParkingLot`.

### FeeStrategy

`FeeStrategy` defines the policy used to calculate the parking fee.

#### Why does it exist?

Different parking lots may use different pricing models, such as:

- Hourly pricing
- Vehicle-type-based pricing
- Progressive pricing
- Flat-rate pricing

By separating fee calculation from `ParkingLot`, the pricing policy can change independently of the parking workflow.

## Final Class Design
```
abstract class Vehicle {
    -String regnNo
    +Vehicle(String regnNo)
    +getRegnNo() String
    +canParkIn(SpotType spotType) Boolean
}

class Car extends Vehicle {
    +Car(String regnNo)
    +canParkIn(SpotType spotType) Boolean
}

class Motorcycle extends Vehicle {
    +Motorcycle(String regnNo)
    +canParkIn(SpotType spotType) Boolean
}

class Truck extends Vehicle {
    +Truck(String regnNo)
    +canParkIn(SpotType spotType) Boolean
}
```
```
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
```
```
class ParkingFloor {
    -List<ParkingSpot> parkingSpots
    +ParkingFloor(List<ParkingSpot> parkingSpots)
    +getParkingSpots() List<ParkingSpot>
}
```
```
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
```
```
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
```
```
class ParkingStrategy {
    +findSpot(List~ParkingFloor~ floors, Vehicle vehicle) ParkingSpot
}
```
```
class FeeStrategy {
    +calculateFee(Ticket ticket, long exitTime) double
}
```
```
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