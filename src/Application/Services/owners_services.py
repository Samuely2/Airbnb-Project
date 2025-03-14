from src.Infrastructure.Models.owners import Owners
from src.database import db

class OwnersServices:
    @staticmethod
    def create_owner(session, name, cpf, address, phone, email, password):
        try:
            # Criando um novo Owner com os dados fornecidos
            owner = Owners(
                name=name,
                cpf=cpf,
                address=address,
                phone=phone,
                email=email,
                password=password
            )

            # Adicionando o Owner à sessão e realizando o commit
            session.add(owner)
            session.commit()

            return owner
        except Exception as e:
            # Se ocorrer algum erro, fazemos rollback na transação
            session.rollback()
            raise e
