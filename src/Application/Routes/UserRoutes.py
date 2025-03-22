from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.database import db
from src.Application.Services.UserServices import UsersService
from src.Infrastructure.Models.UserModel import Users
from src.Domain.enums.typeUsersEnum import TypeUserEnum

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/", methods=["POST"])
@swag_from({
    'summary': 'Create a new user',
    'description': 'This endpoint creates a new user by accepting the user data and saving it to the database.',
    'tags': ['User'],
    'responses': {
        '201': {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad Request - Missing required fields or Invalid user type'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'User data for creation',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'The name of the user', 'required': True},
                    'phone': {'type': 'string', 'description': 'The phone number of the user', 'required': True},
                    'email': {'type': 'string', 'description': 'The email address of the user', 'required': True},
                    'password': {'type': 'string', 'description': 'The password for the user', 'required': True},
                    'address': {'type': 'string', 'description': 'The address of the user', 'required': True},
                    'typeUser': {'type': 'string', 'description': 'The type of the user (e.g., APARTAMENT, ADMIN)', 'required': False, 'default': 'APARTAMENT'}
                },
                'example': {
                    'name': 'John Doe',
                    'phone': '1234567890',
                    'email': 'johndoe@example.com',
                    'password': 'securepassword',
                    'address': '123 Main St',
                    'typeUser': 'APARTAMENT'
                }
            }
        }
    ]
})
def create_user():
    try:
        data = request.json
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        password = data.get("password")
        address = data.get("address")
        typeUser = data.get("typeUser", "APARTAMENT")  # Valor padrão

        if not all([name, phone, email, password, address]):
            return jsonify({"error": "Missing required fields"}), 400

        if typeUser not in TypeUserEnum.__members__:
            return jsonify({"error": "Invalid user type"}), 400

        user = UsersService.create_user(db.session, name, phone, email, password, address, TypeUserEnum[typeUser])
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/", methods=["GET"])
@swag_from({
    'summary': 'Get all users',
    'description': 'This endpoint retrieves all the users from the database.',
    'tags': ['User'],
    'responses': {
        '200': {
            'description': 'List of all users',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'phone': {'type': 'string'},
                        'email': {'type': 'string'},
                        'address': {'type': 'string'},
                        'typeUser': {'type': 'string'}
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_all_users():
    users = Users.query.all()
    user_list = [{
        "id": u.id,
        "name": u.name,
        "phone": u.phone,
        "email": u.email,
        "address": u.address,
        "typeUser": u.typeUser.name
    } for u in users]
    return jsonify(user_list), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
@swag_from({
    'summary': 'Get user details',
    'description': 'This endpoint retrieves details of a specific user by user ID.',
    'tags': ['User'],
    'responses': {
        '200': {
            'description': 'User details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'phone': {'type': 'string'},
                    'email': {'type': 'string'},
                    'address': {'type': 'string'},
                    'typeUser': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'User not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "address": user.address,
        "typeUser": user.typeUser.name
    }), 200

@user_bp.route("/<int:user_id>", methods=["PUT"])
@swag_from({
    'summary': 'Update a user',
    'description': 'This endpoint updates the information of an existing user.',
    'tags': ['User'],
    'responses': {
        '200': {
            'description': 'User updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Bad Request - Invalid user type'
        },
        '404': {
            'description': 'User not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'User data for update',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'The updated name of the user', 'required': False},
                    'phone': {'type': 'string', 'description': 'The updated phone number of the user', 'required': False},
                    'email': {'type': 'string', 'description': 'The updated email address of the user', 'required': False},
                    'address': {'type': 'string', 'description': 'The updated address of the user', 'required': False},
                    'typeUser': {'type': 'string', 'description': 'The updated type of the user (e.g., APARTAMENT, ADMIN)', 'required': False}
                },
                'example': {
                    'name': 'John Updated',
                    'phone': '9876543210',
                    'email': 'johnupdated@example.com',
                    'address': '456 Updated St',
                    'typeUser': 'ADMIN'
                }
            }
        }
    ]
})
def update_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.json
        user.name = data.get("name", user.name)
        user.phone = data.get("phone", user.phone)
        user.email = data.get("email", user.email)
        user.address = data.get("address", user.address)
        typeUser = data.get("typeUser", user.typeUser.name)

        if typeUser not in TypeUserEnum.__members__:
            return jsonify({"error": "Invalid user type"}), 400

        user.typeUser = TypeUserEnum[typeUser]

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@swag_from({
    'summary': 'Delete a user',
    'description': 'This endpoint deletes a specific user by user ID.',
    'tags': ['User'],
    'responses': {
        '200': {
            'description': 'User deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'User not found'
        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def delete_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
