from flask import Blueprint, jsonify, request
from src.Application.Controllers.users_controller import UsersController

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return "Olá, mundo!"

@main_routes.route('/api/users', methods=['POST'])
def create_users():
    data = request.json
    try:
        new_user = UsersController.create_user(data)
        return jsonify({
            'id': new_user.id,
            'name': new_user.name,   
            'phone': new_user.phone,
            'email': new_user.email
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400