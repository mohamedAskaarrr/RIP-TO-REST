from flask import Flask, jsonify
from flask_restful import Api, Resource
from netmiko import ConnectHandler

app = Flask(__name__)
api = Api(app)

# Router connection details
ROUTERS = {
    'IOU2': {
        'device_type': 'cisco_ios',
        'host': '192.168.100.1',
        'username': 'admin',
        'password': 'cisco'
    },
    'IOU3': {
        'device_type': 'cisco_ios',
        'host': '192.168.100.2',
        'username': 'admin',
        'password': 'cisco'
    }
}

class RIPRoutes(Resource):
    def get(self, router_name):
        connection = ConnectHandler(**ROUTERS[router_name])
        output = connection.send_command("show ip route rip")
        connection.disconnect()
        return {'router': router_name, 'rip_routes': output}

api.add_resource(RIPRoutes, '/rip/<string:router_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/test')
def test():
    return jsonify({"status": "API is working!"})

@app.route('/')
def home():
    return "RIP-to-REST API is running! Use /rip/IOU2 or /rip/IOU3"