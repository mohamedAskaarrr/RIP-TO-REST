import unittest
from app import app

class TestRIPDashboard(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Dynamically generate a valid token by logging in
        response = self.client.post('/login', json={'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)  # Ensure login is successful
        self.token = response.json['token']  # Extract the token from the response

    def test_login(self):
        response = self.client.post('/login', json={'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_get_routers(self):
        response = self.client.get('/routers', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

    def test_add_router(self):
        router_data = {'ip': '192.168.1.1', 'username': 'admin', 'password': 'admin'}
        response = self.client.post('/routers', json=router_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

    def test_validate_rip_routes(self):
        # Example test for validating RIP routes
        ip = '192.168.1.1'
        username = 'admin'
        password = 'admin'
        # Assuming validate_rip_routes is a helper function in app.py
        from app import validate_rip_routes
        routes = validate_rip_routes(ip, username, password)
        self.assertIsInstance(routes, list)

if __name__ == '__main__':
    unittest.main()