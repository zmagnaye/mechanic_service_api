from app import create_app
from app.extensions import db
from app.models import Inventory
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('app.config.TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()
        self.client = self.app.test_client()
    
    # Create (POST: /inventory/)
    def test_create_part_success(self):
        payload = {"name": "Brake Pads", "price": 49.99}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["name"], "Brake Pads")
        self.assertEqual(body["price"], 49.99)

    # Create (POST: /inventory/ -> price not a valid number)
    def test_invalid_creation(self):
        payload = {"name": "Rotor", "price": "number"}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("price", response.get_json())
        self.assertIsInstance(response.get_json()["price"], list)

    # List (GET: /inventory/)
    def test_list_inventory(self):
        self.client.post("/inventory/", json = {"name": "Oil Filter", "price": 9.50})
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertGreaterEqual(len(response.get_json()), 1)

    # Get (GET: /inventory/{id})
    def test_get_inventory(self):
        create_inventory = self.client.post("/inventory/", json = {"name": "Air Filter", "price": 15.00})
        pid = create_inventory.get_json()["id"]
        response = self.client.get(f'/inventory/{pid}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], pid)
    
    # Get (GET: /inventory/{id} => Not found)
    def test_get_inventory_not_found(self):
        response = self.client.get(f'/inventory/9999')
        self.assertEqual(response.status_code, 404)

    # Update (PUT: /inventory/{id})
    def test_update_inventory(self):
        create_inventory = self.client.post("/inventory/", json = {"name": "Spark Plug", "price": 6.25})
        pid = create_inventory.get_json()["id"]
        payload = {"name": "Premium Spark Plug", "price": 7.25}
        response = self.client.put(f'/inventory/{pid}', json = payload)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["name"], "Premium Spark Plug")
        self.assertEqual(body["price"], 7.25)

    # Update (PUT: /inventory/{id} -> Not found)
    def test_update_part_not_found(self):
        response = self.client.put(f'/inventory/9999', json = {"name": "X", "price": 1.00})
        self.assertEqual(response.status_code, 404)

    # Delete attempt (DELETE: /inventory/{id})
    def test_delete_inventory(self):
        create_inventory = self.client.post("/inventory/", json = {"name": "Coolant", "price": 12.50})
        pid = create_inventory.get_json()["id"]
        response = self.client.delete(f'/inventory/{pid}')
        self.assertEqual(response.status_code, 200)
    
    # Delete attempt (DELETE: /inventory/{id} -> Not Found)
    def test_delete_not_found(self):
        response = self.client.delete(f'/inventory/9999')
        self.assertEqual(response.status_code, 404)