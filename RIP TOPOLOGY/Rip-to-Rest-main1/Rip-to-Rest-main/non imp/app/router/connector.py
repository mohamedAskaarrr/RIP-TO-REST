 # app/router/connector.py
import netmiko
import logging

logger = logging.getLogger(__name__)

class RouterConnector:
    """Class to manage connections to network routers."""
    
    def __init__(self, host, username, password, device_type='cisco_ios'):
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type
        self.connection = None
    
    def connect(self):
        """Establish SSH connection to the router."""
        try:
            self.connection = netmiko.ConnectHandler(
                device_type=self.device_type,
                host=self.host,
                username=self.username,
                password=self.password,
            )
            logger.info(f"Connected to router: {self.host}")
            return True
        except Exception as e:
            logger.error(f"Connection failed to {self.host}: {str(e)}")
            return False
    
    def disconnect(self):
        """Close the SSH connection."""
        if self.connection:
            self.connection.disconnect()
            self.connection = None
            logger.info(f"Disconnected from router: {self.host}")
    
    def execute_command(self, command):
        """Execute a command on the router and return the output."""
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            output = self.connection.send_command(command)
            logger.debug(f"Command executed on {self.host}: {command}")
            return output
        except Exception as e:
            logger.error(f"Command execution failed on {self.host}: {str(e)}")
            return None
    
    def get_rip_database(self):
        """Retrieve the RIP routing database."""
        return self.execute_command("show ip rip database")
    
    def get_rip_status(self):
        """Retrieve RIP protocol status."""
        return self.execute_command("show ip protocols | section RIP")
    
    def get_interfaces(self):
        """Get interfaces with RIP enabled."""
        return self.execute_command("show ip interface brief")