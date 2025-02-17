from flask import Blueprint, request, jsonify
from app.services.booking_service import BookingService
from app.utils.validators import BookingSchema
from app.utils.auth import auth_required
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('', methods=['POST'])
@auth_required
def book_seat():
    try:
        current_user = get_jwt_identity()
        user_id = current_user
        print(f"User ID from JWT: {user_id}")
        
        schema = BookingSchema()
        data = schema.load(request.json)
        
        result, status_code = BookingService.book_seat(
            user_id=user_id,
            train_id=data['train_id'],
            source=data['source'],
            destination=data['destination'],
            booking_date=data['booking_date'],
            number_of_seats=data['number_of_seats']
        )
        
        return jsonify(result), status_code
    except ValidationError as e:
        return jsonify({'success': False, 'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@booking_bp.route('/<string:booking_id>', methods=['GET'])
@auth_required
def get_booking_details(booking_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user
        
        result, status_code = BookingService.get_booking_details(booking_id, user_id)
        
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@booking_bp.route('/user', methods=['GET'])
@auth_required
def get_user_bookings():
    try:
        current_user = get_jwt_identity()
        user_id = current_user
        
        result, status_code = BookingService.get_user_bookings(user_id)
        
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500