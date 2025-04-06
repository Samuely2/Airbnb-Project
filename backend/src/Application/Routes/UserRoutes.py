from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import jwt
from src.database import db
from src.Infrastructure.Models.UserModel import User
from src.Domain.enums.typeUsersEnum import TypeUserEnum
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint("user", __name__, url_prefix="/users")

# Chave secreta para JWT - em produção use uma variável de ambiente
SECRET_KEY = "ChaveTeste" 

@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        required_fields = ["name", "phone", "email", "password", "address"]
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Verificar se o email já está cadastrado
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 400

        # Criar hash da senha
        hashed_password = generate_password_hash(data["password"])
        
        # Criar usuário
        user = User(
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            password=hashed_password,
            address=data["address"],
            typeUser=TypeUserEnum(data.get("typeUser", "OWNER"))
        )

        db.session.add(user)
        db.session.commit()

        # Gerar token JWT
        token_payload = {
            "id": user.id,
            "name": user.name,
            "typeUser": user.typeUser.value,
            "exp": datetime.now(timezone.utc) + timedelta(hours=5)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "message": "User registered successfully",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "typeUser": user.typeUser.value
            }
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=data["email"]).first()
        
        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Invalid email or password"}), 401

        # Gerar token JWT (igual ao UserService)
        token_payload = {
            "id": user.id,
            "name": user.name,
            "typeUser": user.typeUser.value,
            "exp": datetime.now(timezone.utc) + timedelta(hours=5)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "typeUser": user.typeUser.value
            }
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/me", methods=["GET"])
def get_current_user():
    try:
        # Verificar token (implementação básica)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
            
        token = auth_header.split(" ")[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = User.query.get(payload["id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "typeUser": user.typeUser.value
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/me", methods=["PUT"])
def update_user():
    try:
        # Verificar token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
            
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        user = User.query.get(payload["id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.json
        
        # Campos atualizáveis
        if "name" in data:
            user.name = data["name"]
        if "phone" in data:
            user.phone = data["phone"]
        if "address" in data:
            user.address = data["address"]
        if "password" in data:
            user.password = generate_password_hash(data["password"])
        
        db.session.commit()
        
        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "typeUser": user.typeUser.value
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500