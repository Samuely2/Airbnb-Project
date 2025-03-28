from flask import Blueprint, request, jsonify
from src.database import db
from src.Application.Services.HallServices import HallServices
from src.Infrastructure.Models.HallModel import Hall
from flasgger import swag_from

hall_bp = Blueprint("hall", __name__, url_prefix="/halls")

@hall_bp.route("/", methods=["POST"])
def create_hall():
    try:
        data = request.json
        name = data.get("name")
        location = data.get("location")
        description = data.get("description")
        fk_owner = data.get("fk_owner")
        fk_typeHall = data.get("fk_typeHall")

        if not all([name, location, fk_owner, fk_typeHall]):
            return jsonify({"error": "Missing required fields"}), 400

        hall = HallServices.create_hall(db.session, name, location, description, fk_owner, fk_typeHall)
        return jsonify({"message": "Hall created successfully", "hall": hall.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/", methods=["GET"])
def get_all_halls():
    try:
        halls = Hall.query.all()
        hall_list = [{"id": h.id, "name": h.name, "location": h.location, "description": h.description} for h in halls]
        return jsonify(hall_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>", methods=["GET"])
def get_hall(hall_id):
    hall = Hall.query.get(hall_id)
    if not hall:
        return jsonify({"error": "Hall not found"}), 404
    return jsonify({
        "id": hall.id, 
        "name": hall.name, 
        "location": hall.location, 
        "description": hall.description
    }), 200


@hall_bp.route("/<int:hall_id>", methods=["PUT"])
def update_hall(hall_id):
    try:
        hall = Hall.query.get(hall_id)
        if not hall:
            return jsonify({"error": "Hall not found"}), 404

        data = request.json
        hall.name = data.get("name", hall.name)
        hall.location = data.get("location", hall.location)
        hall.description = data.get("description", hall.description)

        db.session.commit()
        return jsonify({"message": "Hall updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>", methods=["DELETE"])
def delete_hall(hall_id):
    try:
        hall = Hall.query.get(hall_id)
        if not hall:
            return jsonify({"error": "Hall not found"}), 404

        db.session.delete(hall)
        db.session.commit()
        return jsonify({"message": "Hall deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
