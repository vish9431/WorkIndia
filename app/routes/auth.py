from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import UserRegistrationSchema, UserLoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        schema = UserRegistrationSchema()
        data = schema.load(request.json)
        
        result, status_code = AuthService.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        return jsonify(result), status_code
    except ValidationError as e:
        return jsonify({'success': False, 'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        schema = UserLoginSchema()
        data = schema.load(request.json)
        
        result, status_code = AuthService.login_user(
            username=data['username'],
            password=data['password']
        )
        
        return jsonify(result), status_code
    except ValidationError as e:
        return jsonify({'success': False, 'message': 'Validation error', 'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500