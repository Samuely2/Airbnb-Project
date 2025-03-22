from flask import Blueprint, request, jsonify
from src.database import db
from src.Application.Services.HallServices import HallServices
from src.Infrastructure.Models.HallModel import Hall
from flasgger import swag_from

hall_bp = Blueprint("hall", __name__, url_prefix="/halls")

# Rota para criar o hall com a documentação do Swagger
@hall_bp.route("/", methods=["POST"])
@swag_from({
    'tags': ['Halls'],
    'summary': 'Create a new hall',
    'description': 'Create a new hall with name, location, description, owner, and type of hall.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Hall creation data',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Conference Hall'},
                    'location': {'type': 'string', 'example': 'Building A, Floor 2'},
                    'description': {'type': 'string', 'example': 'A large hall for conferences and events'},
                    'fk_owner': {'type': 'integer', 'example': 1},
                    'fk_typeHall': {'type': 'integer', 'example': 2}
                },
                'required': ['name', 'location', 'fk_owner', 'fk_typeHall']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Hall created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Hall created successfully'},
                    'hall': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'location': {'type': 'string'},
                            'description': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad Request - Missing required fields or invalid data'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def create_hall():
    try:
        data = request.json
        name = data.get("name")
        location = data.get("location")
        description = data.get("description")
        fk_owner = data.get("fk_owner")
        fk_typeHall = data.get("fk_typeHall")

        # Verificando campos obrigatórios
        if not all([name, location, fk_owner, fk_typeHall]):
            return jsonify({"error": "Missing required fields"}), 400

        # Criando o hall
        hall = HallServices.create_hall(db.session, name, location, description, fk_owner, fk_typeHall)
        return jsonify({"message": "Hall created successfully", "hall": hall.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para listar todos os halls com a documentação do Swagger
@hall_bp.route("/", methods=["GET"])
@swag_from({
    'tags': ['Halls'],
    'summary': 'Get all halls',
    'description': 'Retrieve a list of all halls.',
    'responses': {
        '200': {
            'description': 'List of all halls',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'description': {'type': 'string'}
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_all_halls():
    try:
        halls = Hall.query.all()
        hall_list = [{"id": h.id, "name": h.name, "location": h.location, "description": h.description} for h in halls]
        return jsonify(hall_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para obter detalhes de um hall específico com a documentação do Swagger
@hall_bp.route("/<int:hall_id>", methods=["GET"])
@swag_from({
    'tags': ['Halls'],
    'summary': 'Get a hall by ID',
    'description': 'Retrieve details of a hall by its ID.',
    'parameters': [
        {
            'name': 'hall_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the hall to fetch'
        }
    ],
    'responses': {
        '200': {
            'description': 'Hall details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'location': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Hall not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_hall(hall_id):
    hall = Hall.query.get(hall_id)
    if not hall:
        return jsonify({"error": "Hall not found"}), 404
    return jsonify({
        "id": hall.id, 
        "name": hall.name, 
        "location": hall.location, 
        "description": hall.description
    }), 200


# Rota para atualizar um hall existente com a documentação do Swagger
@hall_bp.route("/<int:hall_id>", methods=["PUT"])
@swag_from({
    'tags': ['Halls'],
    'summary': 'Update a hall by ID',
    'description': 'Update an existing hall with new data.',
    'parameters': [
        {
            'name': 'hall_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the hall to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Hall update data',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Updated Conference Hall'},
                    'location': {'type': 'string', 'example': 'Updated Location'},
                    'description': {'type': 'string', 'example': 'Updated description of the hall'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Hall updated successfully'
        },
        '400': {
            'description': 'Bad Request - Invalid data'
        },
        '404': {
            'description': 'Hall not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def update_hall(hall_id):
    try:
        hall = Hall.query.get(hall_id)
        if not hall:
            return jsonify({"error": "Hall not found"}), 404

        data = request.json
        hall.name = data.get("name", hall.name)
        hall.location = data.get("location", hall.location)
        hall.description = data.get("description", hall.description)

        db.session.commit()
        return jsonify({"message": "Hall updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para excluir um hall com a documentação do Swagger
@hall_bp.route("/<int:hall_id>", methods=["DELETE"])
@swag_from({
    'tags': ['Halls'],
    'summary': 'Delete a hall by ID',
    'description': 'Delete an existing hall by its ID.',
    'parameters': [
        {
            'name': 'hall_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the hall to delete'
        }
    ],
    'responses': {
        '200': {
            'description': 'Hall deleted successfully'
        },
        '404': {
            'description': 'Hall not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def delete_hall(hall_id):
    try:
        hall = Hall.query.get(hall_id)
        if not hall:
            return jsonify({"error": "Hall not found"}), 404

        db.session.delete(hall)
        db.session.commit()
        return jsonify({"message": "Hall deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
