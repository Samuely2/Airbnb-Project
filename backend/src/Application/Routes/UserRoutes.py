from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.database import db
from src.Application.Services.UserServices import UsersService
from src.Infrastructure.Models.UserModel import Users
from src.Domain.enums.typeUsersEnum import TypeUserEnum

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/", methods=["POST"])
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
