class Owner:
    def __init__(self, id, name, cpf, address, phone, email):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.address = address
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Owner(id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address}, phone={self.phone}, email={self.email})"

    @classmethod
    def from_dict(cls, data):
        """Método para converter um dicionário em um objeto Owner."""
        # Adicionando validações simples antes de criar a instância
        required_fields = ['id', 'name', 'cpf', 'address', 'phone', 'email']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise ValueError(f"Campos ausentes: {', '.join(missing_fields)}")
        
        return cls(
            id=data['id'],
            name=data['name'],
            cpf=data['cpf'],
            address=data['address'],
            phone=data['phone'],
            email=data['email']
        )
