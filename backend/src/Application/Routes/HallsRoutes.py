from flask import Blueprint, request, jsonify
from src.Infrastructure.Models.ReservationModel import Reservation
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
        
        updatable_fields = ["name", "description", "capacity", "price_per_hour", 
                          "address", "amenities", "images", "is_active", "unavailable_dates"]
        
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
        hall.is_active = False
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
            
        # Verificar conflitos com datas indisponíveis
        hall = Hall.query.get_or_404(hall_id)
        start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Verificar períodos indisponíveis
        for period in hall.unavailable_dates or []:
            period_start = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
            period_end = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
            
            if not (end_dt < period_start or start_dt > period_end):
                return jsonify({
                    "is_available": False,
                    "reason": "period_unavailable",
                    "conflicting_period": period
                }), 200
        
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

@hall_bp.route("/<int:hall_id>/unavailable_dates", methods=["POST"])
def add_unavailable_dates(hall_id):
    try:
        data = request.get_json()
        hall = Hall.query.get_or_404(hall_id)
        
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
        
        if start_date > end_date:
            return jsonify({"error": "Data inicial não pode ser maior que data final"}), 400
        
        new_period = {
            "start_date": data['startDate'],
            "end_date": data['endDate'],
            "added_at": datetime.utcnow().isoformat()
        }
        
        if not hall.unavailable_dates:
            hall.unavailable_dates = []
        
        # Verifica sobreposição com períodos existentes
        for period in hall.unavailable_dates:
            existing_start = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
            existing_end = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
            
            if not (end_date < existing_start or start_date > existing_end):
                return jsonify({
                    "error": "Período sobreposto com data já indisponível",
                    "conflicting_period": period
                }), 400
        
        hall.unavailable_dates.append(new_period)
        db.session.commit()
        
        return jsonify({
            "message": "Período de indisponibilidade adicionado com sucesso",
            "unavailable_dates": hall.unavailable_dates
        }), 200
        
    except ValueError as e:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>/unavailable_dates", methods=["GET"])
def get_unavailable_dates(hall_id):
    try:
        hall = Hall.query.get_or_404(hall_id)
        return jsonify({
            "unavailable_dates": hall.unavailable_dates or []
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hall_bp.route("/<int:hall_id>/unavailable_dates", methods=["DELETE"])
def remove_unavailable_dates(hall_id):
    try:
        data = request.get_json()
        hall = Hall.query.get_or_404(hall_id)
        
        if not hall.unavailable_dates:
            return jsonify({"error": "Nenhuma data indisponível cadastrada"}), 404
            
        updated_dates = [
            period for period in hall.unavailable_dates 
            if not (period['start_date'] == data['startDate'] and period['end_date'] == data['endDate'])
        ]
        
        if len(updated_dates) == len(hall.unavailable_dates):
            return jsonify({"error": "Período não encontrado"}), 404
            
        hall.unavailable_dates = updated_dates
        db.session.commit()
        
        return jsonify({
            "message": "Período removido com sucesso",
            "unavailable_dates": hall.unavailable_dates
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500