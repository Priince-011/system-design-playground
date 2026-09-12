from enum import Enum


class TicketStatus(Enum):
    """Ticket lifecycle states.
    
    Transitions:
    ACTIVE -> PAID -> CLOSED
    """
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    CLOSED = "CLOSED"
