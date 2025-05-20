import paramiko

router_ip = "192.168.1.1"  # replace with your router IP
username = "admin"
password = "cisco"

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(router_ip, username=username, password=password)
    print("SSH Connection Successful!")

    # Send a command
    stdin, stdout, stderr = ssh.exec_command("show ip route")
    print(stdout.read().decode())

    ssh.close()
except Exception as e:
    print(f"Connection failed: {e}")