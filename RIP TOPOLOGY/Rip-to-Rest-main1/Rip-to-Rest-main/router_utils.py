from netmiko import ConnectHandler
from typing import Dict, List
import os

# Set this to True to enable simulation mode (no actual router connections)
SIMULATION_MODE = True

class RouterConnection:
    def __init__(self, router_ip: str, username: str = "", password: str = "cisco"):
        self.device = {
            "device_type": "cisco_ios_telnet",  # Using Telnet for Packet Tracer
            "host": router_ip,
            "username": "",  # Usually empty for Packet Tracer basic setups
            "password": "cisco",
        }

    def get_rip_routes(self) -> List[Dict]:
        """Get RIP routes from the router"""
        if SIMULATION_MODE:
            # Return simulated data
            return [
                {"network": "192.168.10.0/24", "distance": "120", "metric": "1", "next_hop": "192.168.1.2"},
                {"network": "192.168.20.0/24", "distance": "120", "metric": "2", "next_hop": "192.168.1.3"}
            ]
        
        try:
            with ConnectHandler(**self.device) as net_connect:
                output = net_connect.send_command("show ip route rip", use_textfsm=True)
                return output if output else []
        except Exception as e:
            print(f"Error connecting to router: {str(e)}")
            return []

    def get_rip_neighbors(self) -> List[Dict]:
        """Get RIP neighbors from the router"""
        if SIMULATION_MODE:
            # Return simulated data
            return [
                {"neighbor": "192.168.1.2", "interface": "GigabitEthernet0/0", "uptime": "00:10:30"},
                {"neighbor": "192.168.1.3", "interface": "GigabitEthernet0/1", "uptime": "00:05:15"}
            ]
        
        try:
            with ConnectHandler(**self.device) as net_connect:
                output = net_connect.send_command("show ip protocols | section Routing Protocol is rip", use_textfsm=True)
                return output if output else []
        except Exception as e:
            print(f"Error connecting to router: {str(e)}")
            return []
            
    def set_rip_version(self, version: str) -> Dict:
        """Configure RIP version on the router"""
        if SIMULATION_MODE:
            # Just return success in simulation mode
            return {"status": "success", "message": f"[SIMULATION] RIP version {version} configured successfully on {self.device['host']}"}
        
        try:
            with ConnectHandler(**self.device) as net_connect:
                # Enter configuration mode
                net_connect.config_mode()
                
                # Configure RIP version
                commands = [
                    "router rip",
                    f"version {version}"
                ]
                output = net_connect.send_config_set(commands)
                
                # Save configuration
                net_connect.save_config()
                
                return {"status": "success", "message": f"RIP version {version} configured successfully"}
        except Exception as e:
            print(f"Error configuring RIP version: {str(e)}")
            return {"status": "error", "message": str(e)}

# Define your router IPs from Packet Tracer simulation
ROUTER_IPS = [
    "192.168.1.1",
    "192.168.3.1"
    # Add more router IPs as needed
]

# Module level functions that app.py calls
def get_rip_routes(router_ip: str, username: str, password: str) -> List[Dict]:
    """Get RIP routes from a router"""
    conn = RouterConnection(router_ip)
    conn.device["username"] = username
    conn.device["password"] = password
    return conn.get_rip_routes()

def get_rip_neighbors(router_ip: str, username: str, password: str) -> List[Dict]:
    """Get RIP neighbors from a router"""
    conn = RouterConnection(router_ip)
    conn.device["username"] = username
    conn.device["password"] = password
    return conn.get_rip_neighbors()

def set_rip_version(router_ip: str, username: str, password: str, version: str) -> Dict:
    """Configure RIP version on a router"""
    conn = RouterConnection(router_ip)
    conn.device["username"] = username
    conn.device["password"] = password
    return conn.set_rip_version(version) 