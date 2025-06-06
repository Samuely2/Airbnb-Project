from flask import Blueprint, request, jsonify
from src.Domain.enums.reservationStatusEnum import ReservationStatusEnum
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

@reservation_bp.route("/<int:reservation_id>/status", methods=["PUT"])
def update_reservation_status(reservation_id):
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        data = request.json
        
        if not data or "status" not in data:
            return jsonify({"error": "O campo 'status' é obrigatório"}), 400
        
        received_status = data["status"]

        valid_statuses = [item.value for item in ReservationStatusEnum]
        if received_status not in valid_statuses:
            return jsonify({"error": f"Status inválido. Deve ser um de: {', '.join(valid_statuses)}"}), 400
    
        status_as_enum_member = ReservationStatusEnum(received_status)
        
        reservation.status = status_as_enum_member
        
        db.session.commit()
        
        return jsonify({
            "message": "Status da reserva atualizado com sucesso",
            "reservation": reservation.to_dict() 
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500