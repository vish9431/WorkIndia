from flask import Blueprint, request, jsonify
from app.services.train_service import TrainService
from app.utils.validators import TrainSchema
from app.utils.auth import admin_required
from marshmallow import ValidationError
from datetime import datetime

train_bp = Blueprint('train', __name__)

@train_bp.route('', methods=['POST'])
@admin_required
def add_train():
    try:
        schema = TrainSchema()
        data = schema.load(request.json)
        
        result, status_code = TrainService.add_train(data)
        
        return jsonify(result), status_code
    except ValidationError as e:
        return jsonify({'success': False, 'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@train_bp.route('/availability', methods=['GET'])
def get_availability():
    try:
        source = request.args.get('source')
        destination = request.args.get('destination')
        date_str = request.args.get('date')
        
        if not all([source, destination, date_str]):
            return jsonify({
                'success': False,
                'message': 'Source, destination, and date are required'
            }), 400
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        result, status_code = TrainService.get_availability(source, destination, date)
        
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@train_bp.route('/<int:train_id>/seats', methods=['PUT'])
@admin_required
def update_train_seats(train_id):
    try:
        new_total_seats = request.json.get('total_seats')
        
        if not new_total_seats or not isinstance(new_total_seats, int) or new_total_seats <= 0:
            return jsonify({
                'success': False,
                'message': 'Valid positive total_seats required'
            }), 400
        
        result, status_code = TrainService.update_train_seats(train_id, new_total_seats)
        
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500