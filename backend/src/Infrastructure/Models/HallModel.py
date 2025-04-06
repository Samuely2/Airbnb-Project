from src.database import db

class Hall(db.Model):
    __tablename__ = "Halls"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    amenities = db.Column(db.JSON, nullable=True)  # Lista de comodidades (ex: ["WiFi", "Estacionamento"])
    images = db.Column(db.JSON, nullable=True)  # URLs das imagens
    fk_owner = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "capacity": self.capacity,
            "price_per_hour": self.price_per_hour,
            "address": self.address,
            "amenities": self.amenities or [],
            "images": self.images or [],
            "owner_id": self.fk_owner,
            "is_active": self.is_active
        }

    def __init__(self, name, capacity, price_per_hour, address, fk_owner, 
                 description=None, amenities=None, images=None):
        self.name = name
        self.capacity = capacity
        self.price_per_hour = price_per_hour
        self.address = address
        self.fk_owner = fk_owner
        self.description = description
        self.amenities = amenities
        self.images = images