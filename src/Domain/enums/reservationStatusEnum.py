from enum import Enum

class ReservationStatusEnum(Enum):
    PENDING = "pendente"
    CONFIRMED = "confirmada"
    CANCELED = "cancelada"