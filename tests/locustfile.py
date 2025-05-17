from locust import HttpUser, task, between

class ApiUser(HttpUser):
    host = "http://196.136.48.164"  # <-- Add this line (use your actual API host)
    wait_time = between(1, 5)
    token = None

    def on_start(self):
        # Get authentication token
        response = self.client.post("/api/v1/auth/token", 
                                    auth=("test_user", "test_password"))
        self.token = response.json()["token"]

    @task
    def get_routers(self):
        self.client.get("/api/v1/routers", 
                       headers={"Authorization": f"Bearer {self.token}"})

    @task
    def get_rip_routes(self):
        self.client.get("/api/v1/routers/R1/rip/routes", 
                       headers={"Authorization": f"Bearer {self.token}"})