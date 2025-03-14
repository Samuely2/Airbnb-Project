from src.Application.Services import users_services
from src.database import db

class UsersController:
    @staticmethod   
    def create_user(data):
        try:
            new_user = users_services.UsersServices.create_user(
                session=db.session,
                name=data['name'],           
                phone=data['phone'],
                email=data['email'],
                password=data['password']
            )
            return new_user
        except Exception as e:
            raise e