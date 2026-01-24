from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user = get_jwt_identity()
        except:
            return jsonify({"error": "Unauthorized or invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated
