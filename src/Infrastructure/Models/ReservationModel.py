from flask_sqlalchemy import SQLAlchemy
from src.Domain.enums.reservationStatusEnum import ReservationStatusEnum


db = SQLAlchemy()

class Reservation(db.Model):
    __tablename__ = "Reservations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_hall = db.Column(db.Integer, db.ForeignKey("Halls.id"), nullable=False)
    fk_user = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    status = db.Column(db.Enum(ReservationStatusEnum), default=ReservationStatusEnum.PENDING, nullable=False)

    hall = db.relationship("Halls", backref="reservations")
    user = db.relationship("Users", backref="reservations")

    def __init__(self, fk_hall, fk_user, start_date, end_date, status=ReservationStatusEnum.PENDING):
        self.fk_hall = fk_hall
        self.fk_user = fk_user
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
