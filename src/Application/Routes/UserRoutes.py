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
    'description': 'Creates a new user and saves it to the database.',
    'tags': ['User'],
    'responses': {
        '201': {'description': 'User created successfully'},
        '400': {'description': 'Missing required fields or invalid user type'},
        '500': {'description': 'Internal Server Error'}
    }
})
def create_user():
    try:
        data = request.json
        required_fields = ["name", "phone", "email", "password", "address"]

        if not all(data.get(field) for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        typeUser = data.pop("typeUser", "Dono")
        typeUserEnum = next((member for member in TypeUserEnum if member.value == typeUser), None)

        if not typeUserEnum:
            return jsonify({"error": "Invalid user type"}), 400

        user = UsersService.create_user(db.session, **data, typeUser=typeUserEnum)
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/", methods=["GET"])
@swag_from({
    'summary': 'Get all users',
    'description': 'Retrieves all users from the database.',
    'tags': ['User'],
    'responses': {
        '200': {'description': 'List of all users'},
        '500': {'description': 'Internal Server Error'}
    }
})
def get_all_users():
    users = Users.query.all()
    return jsonify([
        {"id": u.id, "name": u.name, "phone": u.phone, "email": u.email, "address": u.address, "typeUser": u.typeUser.name}
        for u in users
    ]), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
@swag_from({
    'summary': 'Get user details',
    'description': 'Retrieves details of a specific user by ID.',
    'tags': ['User'],
    'responses': {
        '200': {'description': 'User details'},
        '404': {'description': 'User not found'},
        '500': {'description': 'Internal Server Error'}
    }
})
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id, "name": user.name, "phone": user.phone, "email": user.email,
        "address": user.address, "typeUser": user.typeUser.name
    }), 200

@user_bp.route("/<int:user_id>", methods=["PUT"])
@swag_from({
    'summary': 'Update a user',
    'description': 'Updates the information of an existing user.',
    'tags': ['User'],
    'responses': {
        '200': {'description': 'User updated successfully'},
        '400': {'description': 'Invalid user type'},
        '404': {'description': 'User not found'},
        '500': {'description': 'Internal Server Error'}
    }
})
def update_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.json
        typeUser = data.get("typeUser", user.typeUser.name)
        if typeUser not in TypeUserEnum.__members__:
            return jsonify({"error": "Invalid user type"}), 400

        for key, value in data.items():
            if hasattr(user, key) and value:
                setattr(user, key, value)

        user.typeUser = TypeUserEnum[typeUser]
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@swag_from({
    'summary': 'Delete a user',
    'description': 'Deletes a user by ID.',
    'tags': ['User'],
    'responses': {
        '200': {'description': 'User deleted successfully'},
        '404': {'description': 'User not found'},
        '500': {'description': 'Internal Server Error'}
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
