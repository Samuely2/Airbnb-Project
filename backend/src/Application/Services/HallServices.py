from src.Infrastructure.Models.HallModel import Hall
from src.Infrastructure.Models.UserModel import Users
from src.Infrastructure.Models.TypeHallModel import TypeHall

class HallServices:
    @staticmethod
    def create_hall(session, name, location, description, fk_owner, fk_typeHall):
        try:
            owner = Users.query.get(fk_owner)
            type_hall = TypeHall.query.get(fk_typeHall)

            if not owner:
                raise ValueError("Owner not found")
            if not type_hall:
                raise ValueError("TypeHall not found")

            hall = Hall(
                name=name,
                location=location,
                description=description,
                fk_owner=fk_owner,
                fk_typeHall=fk_typeHall
            )

            session.add(hall)
            session.commit()

            return hall
        except Exception as e:
            session.rollback()
            raise e
