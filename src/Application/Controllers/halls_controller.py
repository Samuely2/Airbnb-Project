from flask import request, jsonify
from src.Application.Services.hall_services import HallServices
from src.database import db

class HallController:
    @staticmethod
    def create_hall():
        try:
            # Obtendo os dados da requisição (supondo que seja uma requisição POST com dados JSON)
            data = request.get_json()

            # Verificando se todos os dados necessários foram passados
            required_fields = ['name', 'type', 'description', 'address', 'owner_id', 'contractor_id']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"'{field}' is required"}), 400

            # Chamando o serviço para criar o Hall
            new_hall = HallServices.create_hall(
                session=db.session,
                name=data['name'],
                type=data['type'],
                description=data['description'],
                address=data['address'],
                owner_id=data['owner_id'],
                contractor_id=data['contractor_id']
            )

            # Retornando a resposta com o Hall criado
            return jsonify({
                "message": "Hall created successfully",
                "hall": {
                    "id": new_hall.id,
                    "name": new_hall.name,
                    "type": new_hall.type,
                    "description": new_hall.description,
                    "address": new_hall.address,
                    "owner_id": new_hall.owner_id,
                    "contractor_id": new_hall.contractor_id
                }
            }), 201

        except Exception as e:
            # Caso ocorra algum erro, retornamos uma mensagem de erro com o status 500
            return jsonify({"error": str(e)}), 500
