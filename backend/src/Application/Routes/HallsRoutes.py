from flask import Blueprint, request, jsonify
from src.database import db
from src.Infrastructure.Models.HallModel import Hall
from datetime import datetime
from flasgger import swag_from

hall_bp = Blueprint("hall", __name__, url_prefix="/halls")

@hall_bp.route("/", methods=["POST"])
def create_hall():
    try:
        data = request.json
        required_fields = ["name", "capacity", "price_per_hour", "address", "fk_owner"]
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        hall = Hall(
            name=data["name"],
            capacity=data["capacity"],
            price_per_hour=data["price_per_hour"],
            address=data["address"],
            fk_owner=data["fk_owner"],
            description=data.get("description"),
            amenities=data.get("amenities", []),
            images=data.get("images", [])
        )

        db.session.add(hall)
        db.session.commit()
        
        return jsonify({"message": "Hall created successfully", "hall": hall.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/", methods=["GET"])
def get_all_halls():
    try:
        # Adicionando filtros básicos
        owner_id = request.args.get("owner_id")
        min_capacity = request.args.get("min_capacity")
        
        query = Hall.query.filter_by(is_active=True)
        
        if owner_id:
            query = query.filter_by(fk_owner=owner_id)
        if min_capacity:
            query = query.filter(Hall.capacity >= min_capacity)
            
        halls = query.all()
        return jsonify([h.to_dict() for h in halls]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>", methods=["GET"])
def get_hall(hall_id):
    try:
        hall = Hall.query.get_or_404(hall_id)
        return jsonify(hall.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404 if "404" in str(e) else 500

@hall_bp.route("/<int:hall_id>", methods=["PUT"])
def update_hall(hall_id):
    try:
        hall = Hall.query.get_or_404(hall_id)
        data = request.json
        
        # Campos atualizáveis
        updatable_fields = ["name", "description", "capacity", "price_per_hour", 
                          "address", "amenities", "images", "is_active"]
        
        for field in updatable_fields:
            if field in data:
                setattr(hall, field, data[field])
        
        db.session.commit()
        return jsonify({"message": "Hall updated successfully", "hall": hall.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>", methods=["DELETE"])
def delete_hall(hall_id):
    try:
        hall = Hall.query.get_or_404(hall_id)
        hall.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({"message": "Hall deactivated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>/availability", methods=["GET"])
def check_availability(hall_id):
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        
        if not start_date or not end_date:
            return jsonify({"error": "Both start_date and end_date are required"}), 400
            
        # Verificar conflitos de reserva
        conflicting_reservations = Reservation.query.filter(
            Reservation.fk_hall == hall_id,
            Reservation.status.in_(["PENDING", "CONFIRMED"]),
            Reservation.start_date < end_date,
            Reservation.end_date > start_date
        ).count()
        
        is_available = conflicting_reservations == 0
        
        return jsonify({
            "is_available": is_available,
            "conflicting_reservations": conflicting_reservations
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500