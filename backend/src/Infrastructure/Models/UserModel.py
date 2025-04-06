from src.database import db
from src.Domain.enums.typeUsersEnum import TypeUserEnum

class User(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)    
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    typeUser = db.Column(db.Enum(TypeUserEnum), nullable=False, default=TypeUserEnum.OWNER)
    profile_picture = db.Column(db.String(255), nullable=True) 
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "typeUser": self.typeUser.value,
            "profile_picture": self.profile_picture,
            "is_active": self.is_active
        }

    def __init__(self, name, phone, email, password, address, typeUser, profile_picture=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.address = address
        self.typeUser = typeUser
        self.profile_picture = profile_picture