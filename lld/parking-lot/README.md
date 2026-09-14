# Designing a Parking Lot System

## Requirements

1. System supports different vehicle types: motorcycle, car, truck
2. System supports multiple floors with different parking spots
3. System automatically assigns available compatible spots
4. System issues a ticket at entry
5. When vehicle exits:
   - System validates ticket
   - Calculates fee based on parking duration and vehicle type
   - Frees the parking spot
6. System rejects entry if no compatible spot available
7. System rejects exit if ticket invalid or already used
8. System should be extensible to various parking and fee calculation strategies

## Out of Scope

- Payment gateway integration
- Advance reservations
- Multi-currency support

---

## Architecture Overview

### Design Principles

1. **Single Responsibility**: Each class has one reason to change
2. **Encapsulation**: Classes manage their own state and expose only necessary operations
3. **Strategy Pattern**: Pluggable algorithms for spot selection and fee calculation
4. **Polymorphism**: Vehicle types and fee strategies use polymorphism over conditionals
5. **Clear Separation of Concerns**: Vehicle describes itself; ParkingSpot determines compatibility

### Vehicle Compatibility Model

**Core Concept**: Vehicle size (not type) determines parking compatibility.

**Size Hierarchy**: `SMALL < MEDIUM < LARGE`

- A SMALL vehicle (motorcycle) fits in SMALL, MEDIUM, or LARGE spots
- A MEDIUM vehicle (car) fits in MEDIUM or LARGE spots
- A LARGE vehicle (truck) fits only in LARGE spots

**Key Design Decision**: 
- `Vehicle` describes itself (type, size, registration)
- `Vehicle` does NOT decide where it can park
- `ParkingSpot` determines compatibility using `can_fit(vehicle)`

This eliminates the coupling between vehicles and spot rules, making the system extensible.

---

## Core Components

### Domain Models

#### Vehicle

Abstract base class for all vehicles.

**Properties:**
- `registration_number`: unique identifier
- `vehicle_type`: VehicleType enum (MOTORCYCLE, CAR, TRUCK)
- `size`: VehicleSize enum (SMALL, MEDIUM, LARGE)

**Concrete Types:**
- `Motorcycle`: inherits with default size SMALL
- `Car`: inherits with default size MEDIUM
- `Truck`: inherits with default size LARGE

**Why separate VehicleType and VehicleSize?**
- VehicleType is descriptive (what kind of vehicle)
- VehicleSize is functional (for parking compatibility)
- Decouples type from parking rules

#### ParkingSpot

Represents a single parking space with full encapsulation of state.

**Properties:**
- `id`: spot identifier
- `size`: SpotSize enum (SMALL, MEDIUM, LARGE)
- `state`: SpotState enum (AVAILABLE, OCCUPIED, OUT_OF_SERVICE)
- `parked_vehicle`: reference to current vehicle (or None)

**Public Methods:**
- `can_fit(vehicle)`: Check if vehicle can fit (without modifying state)
- `park(vehicle)`: Park vehicle with full validation
  - Validates spot is AVAILABLE
  - Validates spot not OUT_OF_SERVICE
  - Validates vehicle fits by size
  - Updates state to OCCUPIED
- `remove_vehicle()`: Remove parked vehicle and return it
  - Returns the removed vehicle
  - Sets state back to AVAILABLE
  - Raises ValueError if spot empty
- `mark_out_of_service()`: Maintenance mode
- `restore_to_service()`: Restore from maintenance

**Why Encapsulation?**
- Prevents invalid state transitions
- Enforces invariants (e.g., incompatible vehicle cannot park)
- Centralizes all spot logic in one place
- Clear, intentional API

#### ParkingFloor

Container for parking spots on a single floor.

**Properties:**
- `id`: floor identifier
- `parking_spots`: list of ParkingSpot objects

**Responsibilities:**
- Own and manage parking spots
- Provide access to spots for strategy queries
- Maintain floor hierarchy

#### ParkingLot

Main orchestrator for all parking operations.

**Properties:**
- `name`: lot name
- `id`: unique lot identifier
- `floors`: list of ParkingFloor objects
- `parking_strategy`: ParkingStrategy instance
- `parking_fee_strategy`: ParkingFeeStrategy instance
- `active_tickets`: dict mapping ticket_id → Ticket

**Key Methods:**
- `enter(vehicle)`: 
  - Delegates to strategy to find spot
  - Parks vehicle on spot
  - Creates and tracks ticket
  - Returns Ticket or None
- `exit(ticket_id)`:
  - Validates ticket exists
  - Marks exit on ticket
  - Removes vehicle from spot
  - Calculates fee
  - Closes ticket
  - Returns fee or None
- `get_available_spots()`: Count available spots
- `get_occupied_spots()`: Count occupied spots

**Why is ParkingLot an Orchestrator?**

Entry flow requires:
1. Find spot (strategy)
2. Park vehicle (spot)
3. Create ticket
4. Track ticket

Exit flow requires:
1. Find ticket
2. Mark exit time
3. Remove vehicle
4. Calculate fee
5. Close ticket

ParkingLot coordinates these without implementing each step.

#### Ticket

Represents a single parking session with full lifecycle.

**Properties:**
- `id`: unique ticket identifier
- `vehicle`: parked vehicle
- `parking_spot`: assigned spot
- `entry_time`: milliseconds since epoch
- `exit_time`: milliseconds since epoch (or None if active)
- `status`: TicketStatus enum (ACTIVE, PAID, CLOSED)

**State Machine:**
```
ACTIVE --mark_exit()--> PAID --close()--> CLOSED
```

**Methods:**
- `mark_exit()`: Transition ACTIVE → PAID
  - Sets exit_time to now
  - Validates ticket is ACTIVE
  - Raises if already exited
- `close()`: Transition PAID → CLOSED
  - Validates ticket is PAID
  - Raises if not PAID

**Why State Validation?**
- Prevents double-exit
- Prevents closing without payment
- Clear, enforced lifecycle

### Enums

#### VehicleType
```
MOTORCYCLE, CAR, TRUCK
```

#### VehicleSize
```
SMALL, MEDIUM, LARGE
```

#### SpotSize
```
SMALL (1), MEDIUM (2), LARGE (3)
```
Numeric values enable comparison for best-fit algorithm.

#### SpotState
```
AVAILABLE, OCCUPIED, OUT_OF_SERVICE
```

#### TicketStatus
```
ACTIVE, PAID, CLOSED
```

---

## Strategy Pattern

### ParkingStrategy

Interface for parking spot selection.

**Method:**
```python
def find_spot(floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]
```

**Implementations:**

#### FirstAvailableStrategy
Returns the first spot that fits the vehicle (FIFO).

Use case: Simple, fast allocation.

#### BestFitStrategy
Returns the smallest spot that fits the vehicle.

Algorithm:
1. Iterate all spots
2. Filter by `can_fit(vehicle)`
3. Select minimum size

Use case: Maximize occupancy by not wasting large spots.

Example:
- Vehicle: MEDIUM
- Available: SMALL, MEDIUM, LARGE, LARGE
- Selects: MEDIUM (not LARGE)

#### FarthestParkingStrategy
Returns the farthest spot (last floor, last spot).

Use case: Spread parking near entrance; keep far spaces for peak times.

### ParkingFeeStrategy

Interface for fee calculation.

**Method:**
```python
def calculate_fee(ticket: Ticket) -> float
```

**Implementations:**

#### FixedFeeStrategy
Flat fee regardless of duration or vehicle type.

#### HourlyFeeStrategy
Duration-based fee: `rate × hours_parked`

Minimum: 1 hour.

#### VehicleTypeHourlyFeeStrategy
Variable rate by vehicle type.

```python
rates = {
    VehicleType.MOTORCYCLE: 5.0,
    VehicleType.CAR: 10.0,
    VehicleType.TRUCK: 15.0
}
```

---

## Parking Flow

### Entry Flow

```
1. Vehicle arrives
2. ParkingLot.enter(vehicle)
3. Strategy finds compatible spot
4. ParkingSpot.park(vehicle) with validation
5. Ticket created with entry time
6. Ticket tracked in active_tickets
7. Return ticket to driver
```

### Exit Flow

```
1. Driver provides ticket ID
2. ParkingLot.exit(ticket_id)
3. Ticket validated and located
4. Ticket.mark_exit() - validates state, sets exit_time
5. ParkingSpot.remove_vehicle() - returns vehicle, frees spot
6. Fee calculated via strategy
7. Ticket.close() - finalizes state
8. Ticket removed from active_tickets
9. Return fee to driver
```

---

## Example Usage

```python
from src.parking_lot.parking_lot import ParkingLot
from src.parking_lot.parking_floor import ParkingFloor
from src.parking_lot.parking_spot import ParkingSpot
from src.parking_lot.spot_size import SpotSize
from src.parking_lot.parking_strategy import BestFitStrategy
from src.parking_lot.parking_fee_strategy import HourlyFeeStrategy
from src.parking_lot.car import Car
from src.parking_lot.motorcycle import Motorcycle

# Setup: 2 floors
floor1 = ParkingFloor("F1")
floor1.add_parking_spot(ParkingSpot("S1", SpotSize.SMALL))
floor1.add_parking_spot(ParkingSpot("M1", SpotSize.MEDIUM))

floor2 = ParkingFloor("F2")
floor2.add_parking_spot(ParkingSpot("L1", SpotSize.LARGE))

# Create parking lot with BestFit strategy, $10/hour
lot = ParkingLot(
    name="Downtown Garage",
    floors=[floor1, floor2],
    parking_strategy=BestFitStrategy(),
    parking_fee_strategy=HourlyFeeStrategy(10.0)
)

# Vehicle enters
car = Car("ABC-1234")
ticket = lot.enter(car)

if ticket:
    print(f"Parked! Ticket: {ticket.get_id()}")
    print(f"Spot: {ticket.get_parking_spot().get_id()}")
else:
    print("No parking available!")

# Vehicle exits
fee = lot.exit(ticket.get_id())
if fee is not None:
    print(f"Fee: ${fee:.2f}")
else:
    print("Invalid ticket!")
```

---

## Test Coverage

Comprehensive test suite with 20+ test cases:

### Unit Tests (test_parking_spot.py)
- ✅ Vehicle-spot size compatibility (9 tests)
- ✅ Parking operations (8 tests)

### Strategy Tests (test_parking_strategy.py)
- ✅ FirstAvailableStrategy
- ✅ BestFitStrategy (correctness of size ordering)
- ✅ FarthestParkingStrategy

### Ticket Tests (test_ticket.py)
- ✅ Ticket lifecycle and state transitions
- ✅ Invalid state transitions

### Integration Tests (test_parking_lot_flow.py)
- ✅ Full entry/exit flow
- ✅ Multiple vehicles
- ✅ Full scenario with 3 vehicles and 2 floors

---

## Design Decisions & Rationale

### 1. Vehicle Size as Primary Compatibility Mechanism

**Decision**: Use `VehicleSize` enum instead of type-based rules in `Vehicle.can_park_in(spot_type)`.

**Rationale**:
- Size is the functional constraint (spots have physical dimensions)
- Type (motorcycle/car/truck) is descriptive, not deterministic
- Eliminates vehicle responsibility for parking rules
- Easier to extend: add VehicleSize values, not new vehicle types

**Before**:
```python
class Vehicle(ABC):
    def can_park_in(self, spot_type: SpotType) -> bool:
        pass  # Each vehicle hardcodes compatibility

class Car(Vehicle):
    def can_park_in(self, spot_type):
        return spot_type in [SpotType.MEDIUM, SpotType.LARGE]
```

**After**:
```python
class Vehicle(ABC):
    size: VehicleSize  # Pure data

class ParkingSpot:
    def can_fit(self, vehicle: Vehicle) -> bool:
        return self.size.can_fit_vehicle_size(vehicle.get_size())
```

### 2. ParkingSpot Encapsulation

**Decision**: Replace direct state manipulation with `park()` and `remove_vehicle()` methods.

**Rationale**:
- Prevents invalid transitions (e.g., parking in occupied spot)
- Centralizes validation logic
- Clear, intentional API
- Easier to add side effects (e.g., logging, notifications)

**Before**:
```python
spot.state = SpotState.OCCUPIED
spot.parked_vehicle = vehicle
```

**After**:
```python
spot.park(vehicle)  # Validates everything
```

### 3. Separate VehicleType and VehicleSize

**Decision**: Two independent enums instead of coupling.

**Rationale**:
- VehicleType answers "what is it?" (motorcycle, car, truck)
- VehicleSize answers "how big is it?" (small, medium, large)
- Fee strategies may care about type; parking cares about size
- Future extensibility: add e-scooter (type) with SMALL size

### 4. Strategy Pattern for Spot Selection

**Decision**: Pluggable strategies instead of hardcoded algorithm.

**Rationale**:
- Real parking lots use different policies
- Enables testing alternative algorithms
- Allows runtime strategy changes
- Clean separation from core logic

### 5. Ticket State Machine

**Decision**: Explicit state transitions (ACTIVE → PAID → CLOSED) with validation.

**Rationale**:
- Prevents double-exit (common bug)
- Clear lifecycle semantics
- Enforces payment-before-close
- Easier to audit and debug

---

## SOLID Principles Checklist

- ✅ **S**ingle Responsibility: Each class has one reason to change
  - Vehicle: describes itself
  - ParkingSpot: manages spot state
  - ParkingStrategy: selects spots
  - ParkingFeeStrategy: calculates fees
  - ParkingLot: orchestrates flow

- ✅ **O**pen/Closed: Extensible without modification
  - Add new strategies without changing existing code
  - Add new vehicle types without changing ParkingSpot

- ✅ **L**iskov Substitution: Strategies are interchangeable
  - Any ParkingStrategy can replace another
  - Any ParkingFeeStrategy can replace another

- ✅ **I**nterface Segregation: Minimal, focused interfaces
  - ParkingStrategy has one method: `find_spot()`
  - ParkingFeeStrategy has one method: `calculate_fee()`

- ✅ **D**ependency Inversion: Depend on abstractions
  - ParkingLot depends on strategy interfaces, not concrete implementations
  - Strategies can be injected

---

## Potential Improvements (Future)

1. **Concurrency**: Add locks/threading for production use
2. **Reservations**: Pre-book spots with expiration
3. **Dynamic Pricing**: Fee varies by time of day, occupancy
4. **Payment Integration**: Process actual payments
5. **Notifications**: Alert drivers of exit validation, payment
6. **Spot Accessibility**: Mark ADA-compliant spots with compatibility logic
7. **Vehicle Damage**: Track incidents and escalation
8. **Analytics**: Usage patterns, revenue reporting
9. **Database**: Persist tickets, vehicles, events
10. **API Gateway**: REST API for entry/exit/status

**Note**: Current implementation is intentionally minimal and interview-friendly. Add features only when requirements demand them.

---

## Running Tests

```bash
cd lld/parking-lot
python -m pytest tests/ -v
```

Expected: 20+ tests passing.
