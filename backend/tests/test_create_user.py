import unittest
import requests

class TestCreateUser(unittest.TestCase):
    
    BASE_URL = "http://localhost:5000/signup"
    
    def test_create_user(self):
        response = requests.post(self.BASE_URL, json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 201)


    def test_create_user_with_existing_email(self):
        response = requests.post(self.BASE_URL, json={
            "username": "anotheruser",
            "email": "existinguser@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 400)
        

    def test_create_user_with_existing_username(self):
        response = requests.post(self.BASE_URL, json={
            "username": "existinguser",
            "email": "anotheruser@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 400)
        

    
    def test_create_user_with_missing_fields(self):
        response = requests.post(self.BASE_URL, json={
            "username": "newuser"
        })

        self.assertEqual(response.status_code, 400)
       

if __name__ == '__main__':
    unittest.main()