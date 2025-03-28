from src.database import db
from src.Domain.enums.typeUsersEnum import TypeUserEnum

class Users(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)    
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    typeUser = db.Column(db.Enum(TypeUserEnum), nullable=False, default=TypeUserEnum.OWNER)

    def __init__(self, name, phone, email, password, address, typeUser):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.address = address
        self.typeUser = typeUser
