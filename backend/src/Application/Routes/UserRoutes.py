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
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        typeUser = data.get("typeUser", "Dono")
        typeUserEnum = next((m for m in TypeUserEnum if m.value == typeUser), None)
        
        if not typeUserEnum:
            return jsonify({"error": "Invalid user type"}), 400

        user_data = {
            "name": data["name"],
            "phone": data["phone"],
            "email": data["email"],
            "password": data["password"],  # Deve ser hashada antes!
            "address": data["address"],
            "typeUser": typeUserEnum
        }

        # Chamada CORRETA ao método:
        user = UsersService.create(db.session, user_data)
        
        return jsonify({
            "message": "User created successfully",
            "user_id": user.id,
            "user": {
                "name": user.name,
                "email": user.email
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        user = UsersService.login_user(db.session, data['email'], data['password'])
        
        if not user:
            return jsonify({"error": "Credenciais inválidas"}), 401

        return jsonify({
            "message": "Login realizado com sucesso",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "typeUser": user.typeUser.value if hasattr(user.typeUser, 'value') else user.typeUser
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500