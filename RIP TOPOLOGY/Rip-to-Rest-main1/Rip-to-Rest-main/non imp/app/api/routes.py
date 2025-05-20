 # app/api/routes.py
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api
from flasgger import swag_from

from app.api import bp
from app.router.connector import RouterConnector
from app.router.parser import RIPDataParser
from app.api.auth import authenticate

api = Api(bp)

@bp.route('/token', methods=['POST'])
def get_token():
    """Get authentication token."""
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    access_token = authenticate(username, password)
    if not access_token:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify(access_token=access_token)

class RIPDatabaseResource(Resource):
    @jwt_required()
    @swag_from('../../docs/rip_database.yml')
    def get(self, router_id=None):
        """Get RIP database from specified router or all routers."""
        routers = []
        if router_id:
            # Get data for specific router
            if router_id not in current_app.config['ROUTER_DEVICES']:
                return {"error": f"Router {router_id} not found"}, 404
            routers = [router_id]
        else:
            # Get data for all routers
            routers = current_app.config['ROUTER_DEVICES']
        
        result = {}
        for router in routers:
            connector = RouterConnector(
                host=router,
                username=current_app.config['ROUTER_USERNAME'],
                password=current_app.config['ROUTER_PASSWORD']
            )
            
            rip_data = connector.get_rip_database()
            parsed_data = RIPDataParser.parse_rip_database(rip_data)
            connector.disconnect()
            
            result[router] = parsed_data
        
        return jsonify(result)

class RIPStatusResource(Resource):
    @jwt_required()
    @swag_from('../../docs/rip_status.yml')
    def get(self, router_id=None):
        """Get RIP protocol status from specified router or all routers."""
        routers = []
        if router_id:
            if router_id not in current_app.config['ROUTER_DEVICES']:
                return {"error": f"Router {router_id} not found"}, 404
            routers = [router_id]
        else:
            routers = current_app.config['ROUTER_DEVICES']
        
        result = {}
        for router in routers:
            connector = RouterConnector(
                host=router,
                username=current_app.config['ROUTER_USERNAME'],
                password=current_app.config['ROUTER_PASSWORD']
            )
            
            rip_status = connector.get_rip_status()
            parsed_status = RIPDataParser.parse_rip_status(rip_status)
            connector.disconnect()
            
            result[router] = parsed_status
        
        return jsonify(result)

# Register API resources
api.add_resource(RIPDatabaseResource, '/rip/database', '/rip/database/<string:router_id>')
api.add_resource(RIPStatusResource, '/rip/status', '/rip/status/<string:router_id>')