from flask import Blueprint, request, jsonify
from src.database import db
from src.Application.Services.ReservationServices import ReservationServices
from src.Infrastructure.Models.ReservationModel import Reservation
from flasgger import swag_from

reservation_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

@reservation_bp.route("/", methods=["POST"])
def create_reservation():
    try:
        data = request.json
        fk_hall = data.get("fk_hall")
        fk_customer = data.get("fk_customer")
        reservation_time = data.get("reservation_time")

        if not all([fk_hall, fk_customer, reservation_time]):
            return jsonify({"error": "Missing required fields"}), 400
        
        reservation = ReservationServices.create_reservation(db.session, fk_hall, fk_customer, reservation_time)
        return jsonify({"message": "Reservation created successfully", "reservation": reservation.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_bp.route("/", methods=["GET"])
def get_all_reservations():
    try:
        reservations = Reservation.query.all()
        reservation_list = [{
            "id": r.id,
            "fk_hall": r.fk_hall,
            "fk_customer": r.fk_customer,
            "reservation_time": r.reservation_time
        } for r in reservations]
        return jsonify(reservation_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_bp.route("/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    return jsonify({
        "id": reservation.id,
        "fk_hall": reservation.fk_hall,
        "fk_customer": reservation.fk_customer,
        "reservation_time": reservation.reservation_time
    }), 200

@reservation_bp.route("/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    try:
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        data = request.json
        reservation.fk_hall = data.get("fk_hall", reservation.fk_hall)
        reservation.fk_customer = data.get("fk_customer", reservation.fk_customer)
        reservation.reservation_time = data.get("reservation_time", reservation.reservation_time)

        db.session.commit()
        return jsonify({"message": "Reservation updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_bp.route("/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    try:
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": "Reservation deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
