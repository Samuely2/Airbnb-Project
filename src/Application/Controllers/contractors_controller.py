from src.Application.Services.contractors_services import ContractorsServices
from src.database import db

class ContractorsController:
    @staticmethod   
    def create_contractor(data):
        try:
            new_contractor = ContractorsServices.create_contractor(
                session=db.session,
                name=data['name'],           
                phone=data['phone'],
                email=data['email'],
                password=data['password']
            )
            return new_contractor
        except Exception as e:
            raise e