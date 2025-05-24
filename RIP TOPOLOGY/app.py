import sys
import os
from flask import Flask, request
from flask_restx import Api, Resource, fields
import json
import jwt
from functools import wraps
import router_utils as ru
from datetime import datetime, timedelta


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)

# Configure Swagger UI with Authorization button
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, 
          title="RIP Dashboard", 
          version="1.0", 
          description="Manage RIP Routers. Authorize using the button above with your JWT token.",
          authorizations=authorizations,
          security='apikey')

DB_FILE = "routers_db.json"
SECRET_KEY = "your_secret_key"
TOKEN_EXPIRY = timedelta(hours=24)

def generate_token(username):
    expiry = datetime.utcnow() + TOKEN_EXPIRY
    return jwt.encode(
        {"username": username, "exp": expiry},
        SECRET_KEY,
        algorithm="HS256"
    )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"msg": "Token is missing"}, 401
            
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
            
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"msg": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"msg": "Invalid token format or signature"}, 401
        except Exception as e:
            return {"msg": f"Authentication error: {str(e)}"}, 401
            
        return f(*args, **kwargs)
    return decorated

def load_routers():
    try:
        with open(DB_FILE, 'r') as f:
            routers = json.load(f)
            print("Loaded routers:", routers)
            return routers
    except:
        return []

def save_routers(routers):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(routers, f, indent=2)
    except Exception as e:
        print(f"Error saving routers: {e}")
        raise RuntimeError(f"Failed to save routers: {e}")

### MODELS ###
login_model = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

router_model = api.model('Router', {
    'ip': fields.String(required=True),
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

rip_config_model = api.model('RIPConfig', {
    'version': fields.String(required=True, enum=['1', '2'])
})

interface_config_model = api.model('InterfaceConfig', {
    'interface': fields.String(required=True),
    'action': fields.String(required=True, enum=['enable', 'disable'])
})

### ROUTES ###
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.json
        if data['username'] == 'admin' and data['password'] == 'admin':
            token = generate_token(data['username'])
            return {
                'token': token,
                'expires_in': TOKEN_EXPIRY.total_seconds()
            }, 200
        return {'msg': 'Invalid credentials'}, 401

@api.route('/routers')
class Routers(Resource):
    @api.expect(router_model)
    @token_required
    def post(self):
        try:
            data = request.json
            if not data or not all(key in data for key in ['ip', 'username', 'password']):
                return {'error': 'Invalid data'}, 400
            
            # Validate router connection
            try:
                ru.get_rip_routes(data['ip'], data['username'], data['password'])
            except Exception as e:
                return {'error': f'Failed to connect to router: {str(e)}'}, 400
            
            routers = load_routers()
            routers.append(data)
            save_routers(routers)
            return {'msg': 'Router added successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @token_required
    def get(self):
        routers = load_routers()
        return {'routers': routers}, 200

@api.route('/routers/<string:ip>/rip/routes')
class RIPRoutes(Resource):
    @token_required
    def get(self, ip):
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        try:
            result = ru.get_rip_routes(ip, router['username'], router['password'])
            return {'routes': result}, 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/routers/<string:ip>/rip/neighbors')
class RIPNeighbors(Resource):
    @token_required
    def get(self, ip):
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        try:
            result = ru.get_rip_neighbors(ip, router['username'], router['password'])
            return {'neighbors': result}, 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/routers/<string:ip>/rip/config')
class RIPConfig(Resource):
    @api.expect(rip_config_model)
    @token_required
    def post(self, ip):
        data = request.json
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        try:
            result = ru.set_rip_version(ip, router['username'], router['password'], data['version'])
            return result, 200 if result['status'] == 'success' else 400
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/routers/<string:ip>/rip/interfaces')
class RIPInterfaces(Resource):
    @api.expect(interface_config_model)
    @token_required
    def post(self, ip):
        data = request.json
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        try:
            result = ru.configure_rip_interface(
                ip,
                router['username'],
                router['password'],
                data['interface'],
                data['action']
            )
            return result, 200 if result['status'] == 'success' else 400
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/routers/<string:ip>/state')
class RouterState(Resource):
    @token_required
    def get(self, ip):
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        try:
            result = ru.get_router_state(ip, router['username'], router['password'])
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)



