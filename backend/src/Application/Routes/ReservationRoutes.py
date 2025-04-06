from flask import Blueprint, request, jsonify
from src.database import db
from src.Infrastructure.Models.ReservationModel import Reservation
from src.Infrastructure.Models.UserModel import User
from src.Infrastructure.Models.HallModel import Hall
from datetime import datetime
from flasgger import swag_from

reservation_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

@reservation_bp.route("/", methods=["POST"])
def create_reservation():
    try:
        data = request.json
        required_fields = ["fk_hall", "fk_user", "start_date", "end_date"]
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Verificar disponibilidade
        conflicting = Reservation.query.filter(
            Reservation.fk_hall == data["fk_hall"],
            Reservation.status.in_(["PENDING", "CONFIRMED"]),
            Reservation.start_date < data["end_date"],
            Reservation.end_date > data["start_date"]
        ).count()
        
        if conflicting > 0:
            return jsonify({"error": "Hall not available for selected dates"}), 400
        
        reservation = Reservation(
            fk_hall=data["fk_hall"],
            fk_user=data["fk_user"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            notes=data.get("notes"),
            status="PENDING"
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            "message": "Reservation created successfully",
            "reservation": reservation.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@reservation_bp.route("/", methods=["GET"])
def get_all_reservations():
    try:
        # Filtros
        user_id = request.args.get("user_id")
        hall_id = request.args.get("hall_id")
        status = request.args.get("status")
        
        query = Reservation.query
        
        if user_id:
            query = query.filter_by(fk_user=user_id)
        if hall_id:
            query = query.filter_by(fk_hall=hall_id)
        if status:
            query = query.filter_by(status=status)
            
        reservations = query.order_by(Reservation.start_date.desc()).all()
        return jsonify([r.to_dict() for r in reservations]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_bp.route("/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        return jsonify(reservation.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404 if "404" in str(e) else 500

@reservation_bp.route("/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        data = request.json
        
        # Atualizar status (para proprietário)
        if "status" in data:
            if data["status"] in ["CONFIRMED", "REJECTED", "CANCELLED"]:
                reservation.status = data["status"]
        
        # Atualizar datas (verificando disponibilidade)
        if "start_date" in data or "end_date" in data:
            new_start = datetime.fromisoformat(data.get("start_date", reservation.start_date.isoformat()))
            new_end = datetime.fromisoformat(data.get("end_date", reservation.end_date.isoformat()))
            
            # Verificar conflitos (excluindo a própria reserva)
            conflicting = Reservation.query.filter(
                Reservation.fk_hall == reservation.fk_hall,
                Reservation.id != reservation.id,
                Reservation.status.in_(["PENDING", "CONFIRMED"]),
                Reservation.start_date < new_end,
                Reservation.end_date > new_start
            ).count()
            
            if conflicting > 0:
                return jsonify({"error": "New dates conflict with existing reservations"}), 400
            
            reservation.start_date = new_start
            reservation.end_date = new_end
        
        if "notes" in data:
            reservation.notes = data["notes"]
        
        db.session.commit()
        return jsonify({
            "message": "Reservation updated successfully",
            "reservation": reservation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@reservation_bp.route("/<int:reservation_id>/status", methods=["PUT"])
def update_reservation_status(reservation_id):
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        data = request.json
        
        if "status" not in data:
            return jsonify({"error": "Status is required"}), 400
        
        valid_statuses = ["PENDING", "CONFIRMED", "REJECTED", "CANCELLED", "COMPLETED"]
        if data["status"] not in valid_statuses:
            return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        
        reservation.status = data["status"]
        db.session.commit()
        
        return jsonify({
            "message": "Reservation status updated successfully",
            "reservation": reservation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500