from src.Infrastructure.Models.users import Users

class UsersServices:
    @staticmethod
    def create_user(session, name, phone, email, password):
        try:            
            users = Users(
                name=name,
                phone=phone,
                email=email,
                password=password
            )

            session.add(users)
            session.commit()

            return users
        except Exception as e:
            session.rollback()
            raise e