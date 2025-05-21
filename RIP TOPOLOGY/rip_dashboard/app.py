# from flask import Flask, request, jsonify
# from flask_restx import Api, Resource, fields
# import json
# from auth import generate_token, token_required
# import router_utils as ru

# app = Flask(__name__)
# api = Api(app, title="RIP Dashboard", version="1.0", description="Manage RIP Routers")

# # In-memory or file-based router DB
# DB_FILE = "routers_db.json"

# def load_routers():
#     try:
#         with open(DB_FILE, 'r') as f:
#             return json.load(f)
#     except:
#         return []

# def save_routers(routers):
#     try:
#         with open(DB_FILE, 'w') as f:
#             json.dump(routers, f, indent=2)
#     except Exception as e:
#         print(f"Error saving routers: {e}")  # Add debug log
#         raise RuntimeError(f"Failed to save routers: {e}")
        

# def validate_rip_routes(ip, username, password):
#     """Validate API responses against actual router CLI outputs."""
#     cli_routes = ru.get_rip_routes(ip, username, password)
#     api_routes = [route['network'] for route in cli_routes]
#     return api_routes        

# ### MODELS ###
# login_model = api.model('Login', {'username': fields.String, 'password': fields.String})
# router_model = api.model('Router', {
#     'ip': fields.String,
#     'username': fields.String,
#     'password': fields.String
# })
# rip_model = api.model('RIPConfig', {
#     'version': fields.String
# })

# ### ROUTES ###
# @api.route('/login')
# class Login(Resource):
#     @api.expect(login_model)
#     def post(self):
#         data = request.json
#         if data['username'] == 'admin' and data['password'] == 'admin':
#             return {'token': generate_token(data['username'])}
#         return {'msg': 'Invalid creds'}, 401

# @api.route('/routers')
# class Routers(Resource):
#     @api.expect(router_model)
#     @token_required
#     def post(self):
#         try:
#             data = request.json
#             if not data or not all(key in data for key in ['ip', 'username', 'password']):
#                 return jsonify({'error': 'Invalid data'}), 400
#             routers = load_routers()
#             routers.append(data)
#             save_routers(routers)
#             return jsonify({'msg': 'Router added'})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# @api.route('/routers/<string:ip>/rip/routes')
# class RIPRoutes(Resource):
#     @token_required
#     def get(self, ip):
#         router = next((r for r in load_routers() if r['ip'] == ip), None)
#         if not router:
#             return jsonify({'msg': 'Router not found'}), 404
#         result = ru.get_rip_routes(ip, router['username'], router['password'])
#         print(f"RIP Routes: {result}")  # Debug log
#         return jsonify({'routes': result})

# @api.route('/routers/<string:ip>/rip/neighbors')
# class RIPNeighbors(Resource):
#     @token_required
#     def get(self, ip):
#         router = next((r for r in load_routers() if r['ip'] == ip), None)
#         if not router:
#             return {'msg': 'Router not found'}, 404
#         result = ru.get_rip_neighbors(ip, router['username'], router['password'])
#         return {'neighbors': result}

# @api.route('/routers/<string:ip>/rip/config')
# class RIPConfig(Resource):
#     @api.expect(rip_model)
#     @token_required
#     def post(self, ip):
#         data = request.json
#         router = next((r for r in load_routers() if r['ip'] == ip), None)
#         if not router:
#             return {'msg': 'Router not found'}, 404
#         result = ru.set_rip_version(ip, router['username'], router['password'], data['version'])
#         return {'config': result}
    

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request
from flask_restx import Api, Resource, fields
import json
from auth import generate_token, token_required
import router_utils as ru

app = Flask(__name__)
api = Api(app, title="RIP Dashboard", version="1.0", description="Manage RIP Routers")

DB_FILE = "routers_db.json"

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
