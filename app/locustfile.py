from locust import HttpUser, task, between

class OrgReadUser(HttpUser):
    # Wait between 0.1 and 1 second
    wait_time = between(0.1, 1)

    @task
    def get_organization(self):
        # We are testing the "Get Organization by Name" endpoint
        # Ensure 'awsm' exists in your DB, or change this to 'org_test'
        target_org = "awsm" 

        with self.client.get(
            "/org/get", 
            params={"organization_name": target_org},
            catch_response=True
        ) as response:
            
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.failure(f"404 Not Found: Organization '{target_org}' does not exist.")
            else:
                response.failure(f"Error: {response.status_code} - {response.text}")
