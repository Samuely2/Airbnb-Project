from src.Domain.enums.typeHallEnum import TypeHallEnum
from src.database import db

class Hall(db.Model):
    __tablename__ = "Halls"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.String(255), nullable=True)

    fk_owner = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    fk_typeHall = db.Column(db.Integer, db.ForeignKey('TypeHall.id'), nullable=False)

    owner = db.relationship("Users", backref="halls") 
    typeHall = db.relationship("TypeHall", backref="halls")

    def __init__(self, name, location, description, fk_owner, fk_typeHall):
        self.name = name
        self.location = location
        self.description = description
        self.fk_owner = fk_owner
        self.fk_typeHall = fk_typeHall