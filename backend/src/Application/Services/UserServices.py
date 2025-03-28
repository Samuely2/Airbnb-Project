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

from src.database import db
from src.Infrastructure.Models.UserModel import Users
from sqlalchemy.exc import SQLAlchemyError

class UsersService:
    @staticmethod
    def login_user(session, email, password):
        try:
            user = session.query(Users).filter_by(email=email).first()
            
            # Verifica se usuário existe e se a senha coincide (comparação direta)
            if user and user.password == password:
                return user
            return None
                
        except SQLAlchemyError as e:
            raise Exception(f"Erro durante o login: {str(e)}")