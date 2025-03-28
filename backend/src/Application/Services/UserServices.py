from src.database import db
from src.Infrastructure.Models.UserModel import Users  # Ajuste para o caminho correto
from src.Domain.enums.typeUsersEnum import TypeUserEnum
from sqlalchemy.exc import SQLAlchemyError

class UsersService:
    @staticmethod
    def create(session, user_data):  # Renomeado para 'create' e aceita dicionário
        try:
            user = Users(
                name=user_data['name'],
                phone=user_data['phone'],
                email=user_data['email'],
                password=user_data['password'],  # Certifique-se de hash essa senha!
                address=user_data['address'],
                typeUser=user_data['typeUser']
            )
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def create_user(session, **kwargs):  # Mantido para compatibilidade
        return UsersService.create(session, kwargs)

    @staticmethod
    def login_user(session, email, password):
        try:
            user = session.query(Users).filter_by(email=email).first()
            
            if user and user.password == password:
                return user
            return None
                
        except SQLAlchemyError as e:
            raise Exception(f"Erro durante o login: {str(e)}")