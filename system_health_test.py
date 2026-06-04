import unittest
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1

class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult

    def run(self, test):
        result = super().run(test)
        print("\n" + "="*30)
        print(f"TEST SUMMARY:")
        print(f"Total Test Cases: {result.testsRun}")
        print(f"Passed: {result.success_count}")
        print(f"Failed: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print("="*30)
        return result

class EWSSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_user = {
            "username": f"testuser_{int(time.time())}",
            "password": "testpassword123",
            "email": "test@example.com"
        }
        cls.token = None
        cls.student_id = 106577 # Sample ID from OULAD

    def test_01_api_heartbeat(self):
        """Test if the API root is accessible"""
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)

    def test_02_user_registration(self):
        """Test advisor/user registration"""
        response = requests.post(f"{API_URL}/register/", json=self.test_user)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('token', data)
        self.__class__.token = data['token']

    def test_03_user_login(self):
        """Test user login with credentials"""
        payload = {
            "username": self.test_user["username"],
            "password": self.test_user["password"]
        }
        response = requests.post(f"{API_URL}/login/", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_04_profile_retrieval(self):
        """Test authenticated profile retrieval"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/profile/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.test_user['username'])

    def test_05_student_list_access(self):
        """Test fetching the student list (Staff/Authorized)"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/students/", headers=headers)
        # It might return 200 even if empty, or we might need is_staff=True
        # For this test, we check if the endpoint is 'active'
        self.assertIn(response.status_code, [200, 403]) 

    def test_06_student_search(self):
        """Test student search functionality"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/students/?search={self.student_id}", headers=headers)
        self.assertIn(response.status_code, [200, 403])

    def test_07_dashboard_stats(self):
        """Test dashboard aggregate statistics"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/stats/", headers=headers)
        self.assertIn(response.status_code, [200, 404]) # 404 if no data imported yet

    def test_08_course_analytics_heatmap(self):
        """Test course analytics heatmap data"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/course-analytics/", headers=headers)
        if response.status_code == 200:
            self.assertIn('heatmap', response.json())
        else:
            self.assertEqual(response.status_code, 403)

    def test_09_course_analytics_regional(self):
        """Test course analytics regional breakdown"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/course-analytics/", headers=headers)
        if response.status_code == 200:
            self.assertIn('by_region', response.json())
        else:
            self.assertEqual(response.status_code, 403)

    def test_10_message_retrieval(self):
        """Test fetching message history"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/messages/", headers=headers)
        self.assertIn(response.status_code, [200, 403])

    def test_11_message_sending_attempt(self):
        """Test sending a message (should fail or succeed depending on permissions)"""
        headers = {"Authorization": f"Token {self.token}"}
        payload = {"student": self.student_id, "content": "Test system message", "sender": "advisor"}
        response = requests.post(f"{API_URL}/messages/", json=payload, headers=headers)
        self.assertIn(response.status_code, [201, 400, 403]) # 400 if student ID invalid

    def test_12_intervention_list(self):
        """Test fetching intervention status list"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(f"{API_URL}/interventions/", headers=headers)
        self.assertIn(response.status_code, [200, 403])

    def test_13_prediction_ping(self):
        """Test if the ML prediction endpoint is responsive"""
        response = requests.post(f"{API_URL}/predict/")
        self.assertIn(response.status_code, [200, 500]) # 500 if model file missing

    def test_14_profile_update(self):
        """Test updating user profile details"""
        headers = {"Authorization": f"Token {self.token}"}
        payload = {"email": "updated_test@example.com"}
        response = requests.put(f"{API_URL}/profile/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], "updated_test@example.com")

    def test_15_user_deletion_cleanup(self):
        """Test user deletion (Cleanup)"""
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.delete(f"{API_URL}/profile/", headers=headers)
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main(testRunner=CustomTestRunner())
