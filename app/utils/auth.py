from flask import request, jsonify, current_app
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        admin_key = request.headers.get('X-Api-Key')
        if not admin_key or admin_key != current_app.config['ADMIN_API_KEY']:
            return jsonify({'message': 'Admin API key is required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"message": "Authorization header missing"}), 401
            
            parts = auth_header.split()
            if parts[0].lower() != 'bearer':
                return jsonify({"message": "Invalid authorization format. Expected 'Bearer token'"}), 401
            if len(parts) == 1:
                return jsonify({"message": "Token missing"}), 401
            
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": f"Authentication error: {str(e)}"}), 401
    return decorated