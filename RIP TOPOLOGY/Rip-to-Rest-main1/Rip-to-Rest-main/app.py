import sys
import os


from flask import Flask, request
from flask_restx import Api, Resource, fields
import json
import jwt
from functools import wraps
import router_utils as ru
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
def generate_token(username):
    return jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"msg": "Token is missing"}, 401
            
        # Handle Bearer prefix if present
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        # Debug message
        print(f"Processing token: {token[:10]}...")
            
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
            return json.load(f)
    except:
        return []

def save_routers(routers):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(routers, f, indent=2)
    except Exception as e:
        print(f"Error saving routers: {e}")
        raise RuntimeError(f"Failed to save routers: {e}")

def validate_rip_routes(ip, username, password):
    cli_routes = ru.get_rip_routes(ip, username, password)
    api_routes = [route['network'] for route in cli_routes]
    return api_routes        

### MODELS ###
login_model = api.model('Login', {'username': fields.String, 'password': fields.String})
router_model = api.model('Router', {
    'ip': fields.String,
    'username': fields.String,
    'password': fields.String
})
rip_model = api.model('RIPConfig', {
    'version': fields.String
})

### ROUTES ###
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.json
        if data['username'] == 'admin' and data['password'] == 'admin':
            return {'token': generate_token(data['username'])}, 200
        return {'msg': 'Invalid creds'}, 401

@api.route('/routers')
class Routers(Resource):
    @api.expect(router_model)
    @token_required
    def post(self):
        try:
            data = request.json
            if not data or not all(key in data for key in ['ip', 'username', 'password']):
                return {'error': 'Invalid data'}, 400
            routers = load_routers()
            routers.append(data)
            save_routers(routers)
            return {'msg': 'Router added'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/routers/<string:ip>/rip/routes')
class RIPRoutes(Resource):
    @token_required
    def get(self, ip):
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        result = ru.get_rip_routes(ip, router['username'], router['password'])
        return {'routes': result}, 200

@api.route('/routers/<string:ip>/rip/neighbors')
class RIPNeighbors(Resource):
    @token_required
    def get(self, ip):
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        result = ru.get_rip_neighbors(ip, router['username'], router['password'])
        return {'neighbors': result}, 200

@api.route('/routers/<string:ip>/rip/config')
class RIPConfig(Resource):
    @api.expect(rip_model)
    @token_required
    def post(self, ip):
        data = request.json
        router = next((r for r in load_routers() if r['ip'] == ip), None)
        if not router:
            return {'msg': 'Router not found'}, 404
        result = ru.set_rip_version(ip, router['username'], router['password'], data['version'])
        return {'config': result}, 200

if __name__ == '__main__':
    app.run(debug=True)
