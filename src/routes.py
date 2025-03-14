from flask import Blueprint, jsonify, request
from src.Application.Controllers.contractors_controller import ContractorsController
from src.Application.Controllers.halls_controller import HallController
from src.Application.Controllers.owners_controller import OwnersController

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return "Olá, mundo!"

@main_routes.route('/api/contractor', methods=['POST'])
def create_contractors():
    data = request.json
    try:
        new_user = ContractorsController.create_contractor(data)
        return jsonify({
            'id': new_user.id,
            'name': new_user.name,   
            'phone': new_user.phone,
            'email': new_user.email
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@main_routes.route('/api/owner', methods=['POST'])
def create_owner():
    data = request.json
    try:
        new_owner = OwnersController.create_owner(data)
        return jsonify({
            'id': new_owner.id,
            'name': new_owner.name,
            'cpf': new_owner.cpf,
            'address': new_owner.address,
            'phone': new_owner.phone,
            'email': new_owner.email
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para criar um novo Hall
@main_routes.route('/api/hall', methods=['POST'])
def create_hall():
    data = request.json
    try:
        new_hall = HallController.create_hall(data)
        return jsonify({
            'id': new_hall.id,
            'name': new_hall.name,
            'type': new_hall.type,
            'description': new_hall.description,
            'address': new_hall.address,
            'owner_id': new_hall.owner_id,
            'contractor_id': new_hall.contractor_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400