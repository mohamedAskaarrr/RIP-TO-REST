 # app/router/parser.py
import re

class RIPDataParser:
    """Parse RIP data from router CLI outputs."""
    
    @staticmethod
    def parse_rip_database(output):
        """Parse the output of 'show ip rip database' command."""
        if not output:
            return []
        
        routes = []
        lines = output.splitlines()
        current_network = None
        
        for line in lines:
            # Match network entries like "1.0.0.0/8    auto-summary"
            network_match = re.match(r'^(\S+)(?:\s+)(.*)$', line.strip())
            if network_match:
                current_network = {
                    'network': network_match.group(1),
                    'type': network_match.group(2),
                    'routes': []
                }
                routes.append(current_network)
                continue
            
            # Match route entries with metrics
            route_match = re.match(r'^\s+\[(\d+)\]\s+via\s+(\S+),\s+(\S+),\s+(\S+)$', line.strip())
            if route_match and current_network:
                current_network['routes'].append({
                    'metric': route_match.group(1),
                    'next_hop': route_match.group(2),
                    'interface': route_match.group(3),
                    'time': route_match.group(4)
                })
        
        return routes
    
    @staticmethod
    def parse_rip_status(output):
        """Parse the output of RIP section from 'show ip protocols' command."""
        if not output:
            return {}
        
        status = {
            'sending_updates': False,
            'receive_version': None,
            'send_version': None,
            'interfaces': [],
            'neighbors': []
        }
        
        # Extract basic information
        version_match = re.search(r'Sending updates every (\d+) seconds', output)
        if version_match:
            status['sending_updates'] = True
            status['update_interval'] = version_match.group(1)
        
        version_match = re.search(r'Version (\d+).*Receive Version (\d+).*Send Version (\d+)', output, re.DOTALL)
        if version_match:
            status['version'] = version_match.group(1)
            status['receive_version'] = version_match.group(2)
            status['send_version'] = version_match.group(3)
        
        # Extract interfaces
        interfaces_section = re.search(r'Routing for Networks:\s+(.*?)(?:\n\n|\Z)', output, re.DOTALL)
        if interfaces_section:
            interfaces = interfaces_section.group(1).strip().split('\n')
            status['interfaces'] = [intf.strip() for intf in interfaces if intf.strip()]
        
        # Extract neighbors
        neighbors_section = re.search(r'Routing Information Sources:\s+(.*?)(?:\n\n|\Z)', output, re.DOTALL)
        if neighbors_section:
            neighbors_lines = neighbors_section.group(1).strip().split('\n')
            for line in neighbors_lines:
                match = re.match(r'\s*Gateway\s+(\S+),\s+last update\s+(\S+)', line)
                if match:
                    status['neighbors'].append({
                        'ip': match.group(1),
                        'last_update': match.group(2)
                    })
        
        return status