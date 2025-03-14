from src.Infrastructure.Models.owners import Owners
from src.Application.Services.owners_services import OwnersServices  # Corrigindo a importação
from src.database import db

class OwnersController:
    @staticmethod   
    def create_owner(data):
        try:
            new_owner = OwnersServices.create_owners(
                session=db.session,
                name=data['name'],
                cpf=data['cpf'],  # Adicionando o CPF
                address=data['address'],  # Adicionando o endereço
                phone=data['phone'],
                email=data['email'],
                password=data['password']
            )
            return new_owner
        except Exception as e:
            # Se ocorrer um erro, lançamos novamente a exceção
            raise e
