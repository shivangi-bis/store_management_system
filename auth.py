# auth.py
from functools import wraps
from flask import request, jsonify

# Simple token (in real projects, you would generate/manage tokens securely)
API_TOKEN = "shivangibis123"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-api-key')
        if not token or token != API_TOKEN:
            return jsonify({"error": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated
