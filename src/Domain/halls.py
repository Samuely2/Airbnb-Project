class Hall:
    def __init__(self, id, name, location, capacity, owner_id):
        self.id = id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.owner_id = owner_id

    def __repr__(self):
        return f"Hall(id={self.id}, name={self.name}, location={self.location}, capacity={self.capacity}, owner_id={self.owner_id})"

    @classmethod
    def from_dict(cls, data):
        """Método para converter um dicionário em um objeto Hall."""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            location=data.get('location'),
            capacity=data.get('capacity'),
            owner_id=data.get('owner_id')
        )
