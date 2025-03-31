from src.Domain.enums.typeHallEnum import TypeHallEnum
from src.database import db

class Hall(db.Model):
    __tablename__ = "Halls"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.String(255), nullable=True)
    typeHall = db.Column(db.Enum(TypeHallEnum), default=TypeHallEnum.HOUSE, nullable=False)
    fk_owner = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    owner = db.relationship("Users", backref="halls") 

    def __init__(self, name, location, description, fk_owner, image):
        self.name = name
        self.location = location
        self.description = description
        self.fk_owner = fk_owner
        self.image = image  