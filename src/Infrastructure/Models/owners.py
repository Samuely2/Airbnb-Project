from src.database import db



class Owners(db.Model):
    __tablename__ = "Owners"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)    
    cpf = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    halls = db.relationship('Hall', backref='owner', lazy=True)

    def __init__(self, name, phone, email, password, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.password = password
