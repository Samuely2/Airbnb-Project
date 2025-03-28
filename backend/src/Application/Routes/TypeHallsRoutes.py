from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.database import db
from src.Application.Services.TypeHallServices import TypeHallServices

typehall_bp = Blueprint("typehall", __name__, url_prefix="/typehalls")

@typehall_bp.route("/", methods=["POST"])
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
def get_all_type_halls():
    try:
        type_halls = TypeHallServices.get_all_type_halls(db.session)
        typehall_list = [{"id": t.id, "name": t.name} for t in type_halls]
        return jsonify(typehall_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@typehall_bp.route("/<int:type_hall_id>", methods=["GET"])
def get_type_hall(type_hall_id):
    try:
        type_hall = TypeHallServices.get_type_hall_by_id(db.session, type_hall_id)
        if not type_hall:
            return jsonify({"error": "TypeHall not found"}), 404
        return jsonify({"id": type_hall.id, "name": type_hall.name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@typehall_bp.route("/<int:type_hall_id>", methods=["PUT"])
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
def delete_type_hall(type_hall_id):
    try:
        TypeHallServices.delete_type_hall(db.session, type_hall_id)
        return jsonify({"message": "TypeHall deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
