from netmiko import ConnectHandler

def connect_to_router(ip, username, password):
    device = {
        'device_type': 'cisco_ios_telnet',
        'ip': ip,
        'username': username,
        'password': password,
    }
    return ConnectHandler(**device)

def get_rip_routes(ip, username, password):
    conn = connect_to_router(ip, username, password)
    output = conn.send_command("show ip route rip")
    conn.disconnect()
    return output

def get_rip_neighbors(ip, username, password):
    conn = connect_to_router(ip, username, password)
    output = conn.send_command("show ip protocols")
    conn.disconnect()
    return output

def set_rip_version(ip, username, password, version='2'):
    conn = connect_to_router(ip, username, password)
    commands = [
        'conf t',
        'router rip',
        f'version {version}',
        'end',
        'wr'
    ]
    output = conn.send_config_set(commands)
    conn.disconnect()
    return output
