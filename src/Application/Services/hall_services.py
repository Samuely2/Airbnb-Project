from src.Infrastructure.Models.hall import Hall  # Importando o modelo Hall
from src.Infrastructure.Models.owners import Owners  # Importando o modelo Owners
from src.Infrastructure.Models.contractors import Contractors  # Importando o modelo Contractors

class HallServices:
    @staticmethod
    def create_hall(session, name, type, description, address, owner_id, contractor_id):
        try:
            # Verificando se o Owner e Contractor existem
            owner = Owners.query.get(owner_id)
            contractor = Contractors.query.get(contractor_id)

            if not owner:
                raise ValueError("Owner not found")
            if not contractor:
                raise ValueError("Contractor not found")

            # Criando um novo Hall (salão)
            hall = Hall(
                name=name,
                type=type,
                description=description,
                address=address,
                owner_id=owner_id,
                contractor_id=contractor_id
            )

            # Adicionando o Hall na sessão e comitando no banco de dados
            session.add(hall)
            session.commit()

            return hall
        except Exception as e:
            # Em caso de erro, desfaz as alterações no banco de dados
            session.rollback()
            raise e
