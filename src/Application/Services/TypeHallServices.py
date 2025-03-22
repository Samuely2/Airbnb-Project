from src.database import db
from src.Infrastructure.Models.TypeHallModel import TypeHall

class TypeHallServices:
    @staticmethod
    def create_type_hall(session, name):
        try:
            type_hall = TypeHall(name=name)
            session.add(type_hall)
            session.commit()
            return type_hall
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_type_hall_by_id(session, type_hall_id):
        return session.query(TypeHall).filter_by(id=type_hall_id).first()

    @staticmethod
    def get_all_type_halls(session):
        return session.query(TypeHall).all()

    @staticmethod
    def update_type_hall(session, type_hall_id, new_name):
        try:
            type_hall = session.query(TypeHall).filter_by(id=type_hall_id).first()
            if not type_hall:
                raise ValueError("TypeHall not found")

            type_hall.name = new_name
            session.commit()
            return type_hall
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def delete_type_hall(session, type_hall_id):
        try:
            type_hall = session.query(TypeHall).filter_by(id=type_hall_id).first()
            if not type_hall:
                raise ValueError("TypeHall not found")

            session.delete(type_hall)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
