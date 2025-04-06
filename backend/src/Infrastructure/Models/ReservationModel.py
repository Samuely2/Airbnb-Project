from datetime import datetime
from src.database import db
from src.Domain.enums.reservationStatusEnum import ReservationStatusEnum

class Reservation(db.Model):
    __tablename__ = "Reservations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_hall = db.Column(db.Integer, db.ForeignKey("Halls.id"), nullable=False)
    fk_user = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    status = db.Column(db.Enum(ReservationStatusEnum), default=ReservationStatusEnum.PENDING, nullable=False)
    notes = db.Column(db.Text, nullable=True)  # Adicionado campo para observações

    # Relacionamentos
    hall = db.relationship("Hall", backref="reservations")
    user = db.relationship("User", backref="reservations")

    def to_dict(self):
        return {
            "id": self.id,
            "hall_id": self.fk_hall,
            "user_id": self.fk_user,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "status": self.status.value,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_name": self.user.name,
            "hall_name": self.hall.name
        }

    def __init__(self, fk_hall, fk_user, start_date, end_date, status=ReservationStatusEnum.PENDING, notes=None):
        self.fk_hall = fk_hall
        self.fk_user = fk_user
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.notes = notes