from src.database import db
from src.Infrastructure.Models.UserModel import Users  # Ajuste para o caminho correto
from src.Domain.enums.typeUsersEnum import TypeUserEnum

class UsersService:
    @staticmethod
    def create_user(session, name, phone, email, password, address, typeUser):
        try:
            user = Users(
                name=name,
                phone=phone,
                email=email,
                password=password,
                address=address,
                typeUser=typeUser
            )

            session.add(user)
            session.commit()

            return user
        except Exception as e:
            session.rollback()
            raise e
