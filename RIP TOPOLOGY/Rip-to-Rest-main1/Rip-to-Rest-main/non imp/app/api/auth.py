from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Invalid token'}), 401
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            if not current_user or not current_user.get('is_admin'):
                return jsonify({'message': 'Admin privileges required'}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Invalid token'}), 401
    return decorated