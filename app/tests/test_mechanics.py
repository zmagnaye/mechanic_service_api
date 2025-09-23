from app import create_app
from app.extensions import db
from app.models import Mechanic
import unittest

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()
        self.client = self.app.test_client()
    
    # Create (POST: /mechanics/)
    def test_create_mechanic_success(self):
        payload = {"name": "Uno Mechanico", "email": "uno@shop.com"}
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["name"], "Uno Mechanico")
        self.assertEqual(body["email"], "uno@shop.com")
    
    # Create (POST: /mechanics/ -> missing email)
    def test_invalid_creation(self):
        payload = { "name": "No Email"} # missing email
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get('email'), ['Missing data for required field.'])

    # List (GET: /mechanics/)
    def test_list_mechanics(self):
        self.client.post("/mechanics/", json = {"name": "Test", "email": "test@shop.com"})
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
    
    # Get (GET: /mechanics/{id})
    def test_get_mechanic(self):
        create_mechanic = self.client.post("/mechanics/", json = {"name": "Test", "email": "test@shop.com"})
        mid = create_mechanic.get_json()["id"]
        response = self.client.get(f'/mechanics/{mid}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], mid)

    # Get (GET: /mechanics/{id} -> Not found)
    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/9999')
        self.assertEqual(response.status_code, 404)

    # Update (PUT: /mechanics/{id})
    def test_update_mechanic(self):
        create_mechanic = self.client.post("/mechanics/", json = {"name": "Test", "email": "test@shop.com"})
        mid = create_mechanic.get_json()["id"]
        payload = {"name": "Update", "email": "test@shop.com"}
        response = self.client.put(f'/mechanics/{mid}', json = payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Update")

    # Update (PUT: /mechanics/{id} -> Not Found)
    def test_update_mechanic_not_found(self):
        response = self.client.put('/mechanics/9999', json = {"name": "X", "email": "x@shop.com"})
        self.assertEqual(response.status_code, 404)
    
    # Delete attempt (DELETE: /mechanics/{id})
    def test_delete_mechanic(self):
        create_mechanic = self.client.post("/mechanics/", json = {"name": "Test", "email": "test@shop.com"})
        mid = create_mechanic.get_json()["id"]
        response = self.client.delete(f'/mechanics/{mid}')
        self.assertEqual(response.status_code, 200)
    
    # Delete attempt (DELETE: /mechanics/{id} -> Not Found)
    def test_delete_not_found(self):
        response = self.client.delete(f'/mechanics/9999')
        self.assertEqual(response.status_code, 404)