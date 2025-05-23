from netmiko import ConnectHandler
from typing import Dict, List, Optional
import os
import json
from datetime import datetime

class RouterConnection:
    def __init__(self, router_ip: str, username: str = "", password: str = "cisco"):
        self.device = {
            "device_type": "cisco_ios_telnet",  # Using Telnet for Packet Tracer
            "host": router_ip,
            "username": username,
            "password": password,
            "timeout": 20,
            "session_log": f"router_{router_ip}.log"
        }
        self.router_state = {
            "last_updated": datetime.now().isoformat(),
            "rip_version": "2",
            "interfaces": [],
            "routes": [],
            "neighbors": []
        }


    def connect(self) -> Optional[ConnectHandler]:
        """Establish connection to router"""
        try:
            return ConnectHandler(**self.device)
        except Exception as e:
            print(f"Error connecting to router {self.device['host']}: {str(e)}")
            return None

    def get_rip_routes(self) -> List[Dict]:
        """Get RIP routes from the router"""
        try:
            conn = self.connect()
            if conn is None:
                raise Exception("Could not connect to router")
            with conn as net_connect:
                # Get RIP routes
                routes_output = net_connect.send_command("show ip route rip", use_textfsm=True)
                
                # Get interface information
                interfaces_output = net_connect.send_command("show ip interface brief", use_textfsm=True)
                
                # Process and combine the data
                routes = []
                if isinstance(routes_output, list):
                    for route in routes_output:
                        route_info = {
                            "network": route.get("network", ""),
                            "distance": route.get("distance", ""),
                            "metric": route.get("metric", ""),
                            "next_hop": route.get("next_hop", ""),
                            "interface": route.get("interface", ""),
                            "last_updated": datetime.now().isoformat()
                        }
                        routes.append(route_info)
                
                self.router_state["routes"] = routes
                self.router_state["interfaces"] = interfaces_output if isinstance(interfaces_output, list) else []
                self.router_state["last_updated"] = datetime.now().isoformat()
                
                return routes
        except Exception as e:
            print(f"Error getting RIP routes: {str(e)}")
            return []

    def get_rip_neighbors(self) -> List[Dict]:
        """Get RIP neighbors from the router"""
        try:
            with self.connect() as net_connect:
                # Get RIP neighbors
                neighbors_output = net_connect.send_command("show ip rip neighbors", use_textfsm=True)
                
                # Get interface status
                interfaces_output = net_connect.send_command("show ip interface brief", use_textfsm=True)
                
                neighbors = []
                if isinstance(neighbors_output, list):
                    for neighbor in neighbors_output:
                        neighbor_info = {
                            "neighbor": neighbor.get("neighbor", ""),
                            "interface": neighbor.get("interface", ""),
                            "uptime": neighbor.get("uptime", ""),
                            "last_update": datetime.now().isoformat()
                        }
                        neighbors.append(neighbor_info)
                
                self.router_state["neighbors"] = neighbors
                self.router_state["last_updated"] = datetime.now().isoformat()
                
                return neighbors
        except Exception as e:
            print(f"Error getting RIP neighbors: {str(e)}")
            return []

    def set_rip_version(self, version: str) -> Dict:
        """Configure RIP version on the router"""
        if version not in ["1", "2"]:
            return {"status": "error", "message": "Invalid RIP version. Must be 1 or 2."}
        
        try:
            with self.connect() as net_connect:
                # Enter configuration mode
                net_connect.config_mode()
                
                # Configure RIP version
                commands = [
                    "router rip",
                    f"version {version}",
                    "no auto-summary"  # Disable auto-summary for better route control
                ]
                output = net_connect.send_config_set(commands)
                
                # Save configuration
                net_connect.save_config()
                
                self.router_state["rip_version"] = version
                self.router_state["last_updated"] = datetime.now().isoformat()
                
                return {
                    "status": "success",
                    "message": f"RIP version {version} configured successfully",
                    "config": output
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def configure_rip_interface(self, interface: str, action: str = "enable") -> Dict:
        """Enable or disable RIP on a specific interface"""
        try:
            with self.connect() as net_connect:
                net_connect.config_mode()
                
                if action == "enable":
                    commands = [
                        f"interface {interface}",
                        "ip rip enable"
                    ]
                else:
                    commands = [
                        f"interface {interface}",
                        "no ip rip enable"
                    ]
                
                output = net_connect.send_config_set(commands)
                net_connect.save_config()
                
                return {
                    "status": "success",
                    "message": f"RIP {action}d on interface {interface}",
                    "config": output
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_router_state(self) -> Dict:
        """Get current router state"""
        return self.router_state

# Module level functions that app.py calls
def get_rip_routes(router_ip: str, username: str, password: str) -> List[Dict]:
    """Get RIP routes from a router"""
    conn = RouterConnection(router_ip, username, password)
    return conn.get_rip_routes()

def get_rip_neighbors(router_ip: str, username: str, password: str) -> List[Dict]:
    """Get RIP neighbors from a router"""
    conn = RouterConnection(router_ip, username, password)
    return conn.get_rip_neighbors()

def set_rip_version(router_ip: str, username: str, password: str, version: str) -> Dict:
    """Configure RIP version on a router"""
    conn = RouterConnection(router_ip, username, password)
    return conn.set_rip_version(version)

def configure_rip_interface(router_ip: str, username: str, password: str, interface: str, action: str = "enable") -> Dict:
    """Configure RIP on a specific interface"""
    conn = RouterConnection(router_ip, username, password)
    return conn.configure_rip_interface(interface, action)

def get_router_state(router_ip: str, username: str, password: str) -> Dict:
    """Get current router state"""
    conn = RouterConnection(router_ip, username, password)
    return conn.get_router_state()
