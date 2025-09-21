from app import create_app
from app.extensions import db
from app.models import Customer
import unittest

class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name="test_user", email="test@email.com", password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.client = self.app.test_client()

    # Create (POST: /customers/)
    def test_create_customer_success(self):
        payload = {"name": "John Doe", "email": "jd@email.com", "password": "123" }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "John Doe")
    
    # Create (POST: /customers/ -> missing email)
    def test_invalid_creation(self):
        payload = { "name": "John Doe","password": "123" } # missing email
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get('email'), ['Missing data for required field.'])

    # List (GET: /customers/)
    def test_list_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
    
    # Login (POST: /customers/login)
    def test_login_customer(self):
        credentials = { "email": "test@email.com", "password": "test"}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn("auth_token", body)
        return body['auth_token']

    # Login (POST: /customers/login)
    def test_invalid_login(self):
        credentials = { "email": "bad_email@email.com", "password": "bad_pw"}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['message'], 'Invalid email or password!')

    # Update (PUT: /customers/{id})
    def test_update_customer(self):
        payload = {"name": "Updated Name","email": "","password": ""}
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put(f'/customers/{self.customer.id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Name') 
        self.assertEqual(response.get_json()['email'], 'test@email.com')
    
    # Update (PUT: /customers/{id} -> Not found)
    def test_update_customer_not_found(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/999999', json={"name": "X"}, headers = headers)
        self.assertEqual(response.status_code, 404)
    
    # Authorized delete attempt (DELETE: /customers/{id})
    def test_delete_customer(self):
        headers = {'Authorization': f"Bearer " + self.test_login_customer()}
        response = self.client.delete(f'/customers/{self.customer.id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    # Unauthorized delete attempt (DELETE: /customers/{id})
    def test_delete_unauthorized(self):
        response = self.client.delete(f'/customers/{self.customer.id}')
        self.assertIn(response.status_code, (401, 403))