from netmiko import ConnectHandler

print("Netmiko is working 🚀")

# === Device list (add your routers here) ===
routers = [
    {
        'name': 'Router0',
        'host': 'ROUTER0_IP',  # 🔧 Replace with actual IP
        'username': 'USERNAME',
        'password': 'PASSWORD',
        'secret': 'ENABLE_PASSWORD',
        'networks': ['192.168.1.0'],
        'passive_interfaces': ['GigabitEthernet0/1']
    },
    {
        'name': 'Router1',
        'host': 'ROUTER1_IP',  # 🔧 Replace with actual IP
        'username': 'USERNAME',
        'password': 'PASSWORD',
        'secret': 'ENABLE_PASSWORD',
        'networks': ['192.168.2.0'],
        'passive_interfaces': ['GigabitEthernet0/1']
    }
]

def configure_rip(router):
    """🚀 Configures RIP v2 on a router + prints results."""
    print(f"🔗 Connecting to {router['name']} at {router['host']}...")

    device = {
        'device_type': 'cisco_ios',
        'host': router['host'],
        'username': router['username'],
        'password': router['password'],
        'secret': router['secret']
    }

    try:
        connection = ConnectHandler(**device)
        connection.enable()

        # 🛠 Build RIP commands
        commands = [
            'router rip',
            'version 2',
            *[f'network {net}' for net in router['networks']],
            *[f'passive-interface {iface}' for iface in router['passive_interfaces']]
        ]

        output = connection.send_config_set(commands)
        print(f"✅ Config applied on {router['name']}:\n{output}")

        connection.disconnect()
    except Exception as e:
        print(f"❌ Failed to configure {router['name']}: {e}")

# === Apply RIP to all routers ===
for router in routers:
    configure_rip(router)
