from src.database import db
from src.Infrastructure.Models.ReservationModel import Reservation
from src.Infrastructure.Models.HallModel import Hall
from src.Infrastructure.Models.UserModel import Users
from src.Domain.enums.reservationStatusEnum import ReservationStatusEnum
from datetime import datetime

class ReservationServices:
    @staticmethod
    def create_reservation(session, fk_hall, fk_user, start_date, end_date, status=ReservationStatusEnum.PENDING):
        try:
            hall = Hall.query.get(fk_hall)
            user = Users.query.get(fk_user)

            if not hall:
                raise ValueError("Hall not found")
            if not user:
                raise ValueError("User not found")

            if start_date >= end_date:
                raise ValueError("Start date must be before end date")

            reservation = Reservation(
                fk_hall=fk_hall,
                fk_user=fk_user,
                start_date=start_date,
                end_date=end_date,
                status=status
            )

            session.add(reservation)
            session.commit()

            return reservation
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_reservation_by_id(session, reservation_id):
        return session.query(Reservation).filter_by(id=reservation_id).first()

    @staticmethod
    def update_reservation_status(session, reservation_id, new_status):
        try:
            reservation = session.query(Reservation).filter_by(id=reservation_id).first()
            if not reservation:
                raise ValueError("Reservation not found")

            reservation.status = new_status
            session.commit()
            return reservation
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def delete_reservation(session, reservation_id):
        try:
            reservation = session.query(Reservation).filter_by(id=reservation_id).first()
            if not reservation:
                raise ValueError("Reservation not found")

            session.delete(reservation)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
