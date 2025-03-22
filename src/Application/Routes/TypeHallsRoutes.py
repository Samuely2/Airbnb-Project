from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.database import db
from src.Application.Services.TypeHallServices import TypeHallServices

typehall_bp = Blueprint("typehall", __name__, url_prefix="/typehalls")

@typehall_bp.route("/", methods=["POST"])
@swag_from({
    'tags': ['TypeHall'],
    'summary': 'Create a new TypeHall',
    'description': 'This endpoint creates a new TypeHall by providing a name.',
    'responses': {
        '201': {
            'description': 'TypeHall created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'type_hall_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad Request - Missing name'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    },
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'The name of the type hall'
        }
    ]
})
def create_type_hall():
    try:
        data = request.json
        name = data.get("name")
        
        if not name:
            return jsonify({"error": "Name is required"}), 400

        type_hall = TypeHallServices.create_type_hall(db.session, name)
        return jsonify({"message": "TypeHall created successfully", "type_hall_id": type_hall.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@typehall_bp.route("/", methods=["GET"])
@swag_from({
    'tags': ['TypeHall'],
    'summary': 'Get all TypeHalls',
    'description': 'This endpoint retrieves all TypeHalls from the database.',
    'responses': {
        '200': {
            'description': 'List of all type halls',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'}
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_all_type_halls():
    try:
        type_halls = TypeHallServices.get_all_type_halls(db.session)
        typehall_list = [{"id": t.id, "name": t.name} for t in type_halls]
        return jsonify(typehall_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@typehall_bp.route("/<int:type_hall_id>", methods=["GET"])
@swag_from({
    'tags': ['TypeHall'],
    'summary': 'Get a TypeHall by ID',
    'description': 'This endpoint retrieves the details of a TypeHall based on its ID.',
    'responses': {
        '200': {
            'description': 'TypeHall details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'TypeHall not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_type_hall(type_hall_id):
    try:
        type_hall = TypeHallServices.get_type_hall_by_id(db.session, type_hall_id)
        if not type_hall:
            return jsonify({"error": "TypeHall not found"}), 404
        return jsonify({"id": type_hall.id, "name": type_hall.name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@typehall_bp.route("/<int:type_hall_id>", methods=["PUT"])
@swag_from({
    'tags': ['TypeHall'],
    'summary': 'Update a TypeHall',
    'description': 'This endpoint updates the name of an existing TypeHall.',
    'responses': {
        '200': {
            'description': 'TypeHall updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'type_hall_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad Request - Missing name'
        },
        '404': {
            'description': 'TypeHall not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    },
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'The new name of the type hall'
        }
    ]
})
def update_type_hall(type_hall_id):
    try:
        data = request.json
        new_name = data.get("name")
        
        if not new_name:
            return jsonify({"error": "Name is required"}), 400

        type_hall = TypeHallServices.update_type_hall(db.session, type_hall_id, new_name)
        return jsonify({"message": "TypeHall updated successfully", "type_hall_id": type_hall.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@typehall_bp.route("/<int:type_hall_id>", methods=["DELETE"])
@swag_from({
    'tags': ['TypeHall'],
    'summary': 'Delete a TypeHall',
    'description': 'This endpoint deletes a TypeHall based on its ID.',
    'responses': {
        '200': {
            'description': 'TypeHall deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'TypeHall not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def delete_type_hall(type_hall_id):
    try:
        TypeHallServices.delete_type_hall(db.session, type_hall_id)
        return jsonify({"message": "TypeHall deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
