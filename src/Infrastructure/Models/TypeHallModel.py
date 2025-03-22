from src.database import db

class TypeHall(db.Model):
    __tablename__ = "TypeHall"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name=name