from flask import Blueprint, request, jsonify
from src.database import db
from src.Application.Services.ReservationServices import ReservationServices
from src.Infrastructure.Models.ReservationModel import Reservation
from flasgger import swag_from

reservation_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

# Rota para criar uma nova reserva com a documentação do Swagger
@reservation_bp.route("/", methods=["POST"])
@swag_from({
    'tags': ['Reservations'],
    'summary': 'Create a new reservation',
    'description': 'Create a new reservation by providing details such as hall, customer, and reservation time.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Reservation creation data',
            'schema': {
                'type': 'object',
                'properties': {
                    'fk_hall': {'type': 'integer', 'example': 1},
                    'fk_customer': {'type': 'integer', 'example': 3},
                    'reservation_time': {'type': 'string', 'example': '2025-03-22T15:00:00'}
                },
                'required': ['fk_hall', 'fk_customer', 'reservation_time']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Reservation created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Reservation created successfully'},
                    'reservation': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'fk_hall': {'type': 'integer'},
                            'fk_customer': {'type': 'integer'},
                            'reservation_time': {'type': 'string'}
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
def create_reservation():
    try:
        data = request.json
        fk_hall = data.get("fk_hall")
        fk_customer = data.get("fk_customer")
        reservation_time = data.get("reservation_time")

        # Verificando campos obrigatórios
        if not all([fk_hall, fk_customer, reservation_time]):
            return jsonify({"error": "Missing required fields"}), 400

        # Criando a reserva
        reservation = ReservationServices.create_reservation(db.session, fk_hall, fk_customer, reservation_time)
        return jsonify({"message": "Reservation created successfully", "reservation": reservation.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para listar todas as reservas com a documentação do Swagger
@reservation_bp.route("/", methods=["GET"])
@swag_from({
    'tags': ['Reservations'],
    'summary': 'Get all reservations',
    'description': 'Retrieve a list of all reservations.',
    'responses': {
        '200': {
            'description': 'List of all reservations',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'fk_hall': {'type': 'integer'},
                        'fk_customer': {'type': 'integer'},
                        'reservation_time': {'type': 'string'}
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_all_reservations():
    try:
        reservations = Reservation.query.all()
        reservation_list = [{
            "id": r.id,
            "fk_hall": r.fk_hall,
            "fk_customer": r.fk_customer,
            "reservation_time": r.reservation_time
        } for r in reservations]
        return jsonify(reservation_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para obter detalhes de uma reserva específica com a documentação do Swagger
@reservation_bp.route("/<int:reservation_id>", methods=["GET"])
@swag_from({
    'tags': ['Reservations'],
    'summary': 'Get a reservation by ID',
    'description': 'Retrieve details of a reservation by its ID.',
    'parameters': [
        {
            'name': 'reservation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the reservation to fetch'
        }
    ],
    'responses': {
        '200': {
            'description': 'Reservation details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'fk_hall': {'type': 'integer'},
                    'fk_customer': {'type': 'integer'},
                    'reservation_time': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Reservation not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    return jsonify({
        "id": reservation.id,
        "fk_hall": reservation.fk_hall,
        "fk_customer": reservation.fk_customer,
        "reservation_time": reservation.reservation_time
    }), 200


# Rota para atualizar uma reserva existente com a documentação do Swagger
@reservation_bp.route("/<int:reservation_id>", methods=["PUT"])
@swag_from({
    'tags': ['Reservations'],
    'summary': 'Update a reservation by ID',
    'description': 'Update an existing reservation with new details.',
    'parameters': [
        {
            'name': 'reservation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the reservation to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Reservation update data',
            'schema': {
                'type': 'object',
                'properties': {
                    'fk_hall': {'type': 'integer', 'example': 1},
                    'fk_customer': {'type': 'integer', 'example': 3},
                    'reservation_time': {'type': 'string', 'example': '2025-03-23T15:00:00'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Reservation updated successfully'
        },
        '400': {
            'description': 'Bad Request - Invalid data'
        },
        '404': {
            'description': 'Reservation not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def update_reservation(reservation_id):
    try:
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        data = request.json
        reservation.fk_hall = data.get("fk_hall", reservation.fk_hall)
        reservation.fk_customer = data.get("fk_customer", reservation.fk_customer)
        reservation.reservation_time = data.get("reservation_time", reservation.reservation_time)

        db.session.commit()
        return jsonify({"message": "Reservation updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para excluir uma reserva com a documentação do Swagger
@reservation_bp.route("/<int:reservation_id>", methods=["DELETE"])
@swag_from({
    'tags': ['Reservations'],
    'summary': 'Delete a reservation by ID',
    'description': 'Delete an existing reservation by its ID.',
    'parameters': [
        {
            'name': 'reservation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the reservation to delete'
        }
    ],
    'responses': {
        '200': {
            'description': 'Reservation deleted successfully'
        },
        '404': {
            'description': 'Reservation not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def delete_reservation(reservation_id):
    try:
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": "Reservation deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
