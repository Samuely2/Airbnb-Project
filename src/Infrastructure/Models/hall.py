from src.Domain.enums.typeHallEnum import TypeHallEnum
from src.database import db

class Hall(db.Model):
    __tablename__ = "Hall"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(TypeHallEnum), nullable=False, default=TypeHallEnum.APARTAMENT)
    description = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('Owners.id'), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('Contractors.id'), nullable=False)
    
    owners = db.relationship('Owners', backref='halls', lazy=True)
    contractor = db.relationship('Contractors', backref='halls', lazy=True)

    def __init__(self, name, type, description, address):
        self.name = name
        self.type = type
        self.description = description
        self.address = address