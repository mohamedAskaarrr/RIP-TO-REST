import requests  # type: ignore

base = "http://127.0.0.1:5000"

# 1. Login
res = requests.post(base + "/login", json={'username': 'admin', 'password': 'admin'})
token = res.json()['token']
headers = {'x-access-token': token}

# 2. Add a router
router = {
    'ip': '192.168.1.1',
    'username': 'cisco',
    'password': 'cisco'
}
requests.post(base + "/routers", headers=headers, json=router)

# 3. Get RIP routes
print(requests.get(base + "/routers/192.168.1.1/rip/routes", headers=headers).json())

# 4. Set RIP version to 2
print(requests.post(base + "/routers/192.168.1.1/rip/config", headers=headers, json={"version": "2"}).json())
