from netmiko import ConnectHandler
# Define your router device
router = {
    "device_type": "cisco_ios_telnet",    # Using Telnet
    "host": "192.168.1.1",                # <<< CHANGE this if your router has a different IP
    "username": "",                       # Empty for Telnet
    "password": "cisco",                  # Password you set on the router
}

# Connect to the router
net_connect = ConnectHandler(**router)

# Send a command
output = net_connect.send_command("show ip route rip")

# Print the output
print(output)



# from flask import Flask, jsonify
# from netmiko import ConnectHandler

# app = Flask(__name__)

# @app.route('/rip/routes', methods=['GET'])
# def get_rip_routes():
#     router = {
#         'device_type': 'cisco_ios',
#         'host': '10.0.0.1',
#         'username': 'admin',
#         'password': 'password',
#     }
#     connection = ConnectHandler(**router)
#     output = connection.send_command('show ip route rip')
#     connection.disconnect()
#     print(output)
#     return jsonify({"rip_routes": output})
    