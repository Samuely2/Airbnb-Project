from datetime import datetime, timedelta, timezone 
import jwt
from src.database import db
from src.Infrastructure.Models.UserModel import Users
from src.Domain.enums.typeUsersEnum import TypeUserEnum
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash  # Adicione esta importação

class UsersService:
    @staticmethod
    def create(session, user_data):
        try:        
            hashed_password = generate_password_hash(user_data['password'])
            
            user = Users(
                name=user_data['name'],
                phone=user_data['phone'],
                email=user_data['email'],
                password=hashed_password,
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
    def create_user(session, **kwargs):
        return UsersService.create(session, kwargs)

    @staticmethod
    def login_user(session, email, password):
        try:
            user = session.query(Users).filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                token_payload = {
                    "id": user.id,
                    "name": user.name,
                    "typeUser": user.typeUser.value,
                    "exp": datetime.now(timezone.utc) + timedelta(hours=5) 
                }
                secret_key = "ChaveTeste"
                token = jwt.encode(token_payload, secret_key, algorithm="HS256")
                
                return token
            
            return None
                
        except SQLAlchemyError as e:
            raise Exception(f"Erro durante o login: {str(e)}")