from src.Infrastructure.Models.contractors import Contractors

class ContractorsServices:
    @staticmethod
    def create_contractor(session, name, phone, email, password):
        try:            
            contractor = Contractors(
                name=name,
                phone=phone,
                email=email,
                password=password
            )

            session.add(contractor)
            session.commit()

            return contractor
        except Exception as e:
            session.rollback()
            raise e