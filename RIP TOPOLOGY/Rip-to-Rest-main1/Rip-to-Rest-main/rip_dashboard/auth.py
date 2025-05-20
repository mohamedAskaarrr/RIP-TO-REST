# import jwt
# from functools import wraps
# from flask import request, jsonify

# SECRET = "RIP_SECRET"

# def generate_token(user):
#     return jwt.encode({"user": user}, SECRET, algorithm="HS256")

# def token_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         token = request.headers.get('x-access-token')
#         if not token:
#             return jsonify({'msg': 'Token missing'}), 401
#         try:
#             jwt.decode(token, SECRET, algorithms=["HS256"])
#         except:
#             return jsonify({'msg': 'Invalid token'}), 401
#         return f(*args, **kwargs)
#     return wrapper


from functools import wraps
from flask import request

# Simple token generator (mock version)
def generate_token(username):
    return f"Bearer {username}-token"

# Token-required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token or not token.startswith("Bearer "):
            return {"msg": "Missing or invalid token"}, 401

        expected_token = generate_token("admin")  # hardcoded for demo
        if token != expected_token:
            return {"msg": "Unauthorized"}, 403

        return f(*args, **kwargs)
    return decorated
