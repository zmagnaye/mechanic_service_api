from app import create_app
from app.extensions import db
from app.models import ServiceTicket
import unittest 

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('app.config.TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()
        self.client = self.app.test_client()
    
    # Create (POST: /service-tickets/)
    def test_create_ticket_success(self):
        create_customer = self.client.post("/customers/", json = {"name": "Cust Mer", "email": "cust_mer@sample.com", "password": "pass123"}) # Customer is needed first
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]
        
        response =  self.client.post("/service-tickets/", json = {"description": "Brake squeal", "customer_id": cid, "status": "open"})
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["description"], "Brake squeal")
        self.assertEqual(body["status"], "open")
        self.assertEqual(body["customer_id"], cid)
        self.assertEqual(body["mechanics"], []) # starts empty
        self.assertEqual(body["parts"], []) # starts empty

    # Create (POST: /service-tickets/ -> invalid customer)
    def test_invalid_creation(self):    
        response = self.client.post("/service-tickets/", json = {"description": "Rattle", "customer_id": 9999})
        self.assertIn(response.status_code, (400, 404))
    
    # List (GET: /service-tickets/)
    def test_list_tickets(self):
        create_customer = self.client.post("/customers/", json = {"name": "A", "email": "a@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]
        self.client.post("/service-tickets/", json = {"description": "First Ticket", "customer_id": cid, "status": "open"})
        response = self.client.get("/service-tickets/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    # Get (GET: /service-tickets/{id})
    def test_get_ticket(self):
        create_customer = self.client.post("/customers/", json = {"name": "B", "email": "b@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]

        create_ticket = self.client.post("/service-tickets/", json = {"description": "Clunk", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]

        response = self.client.get(f"/service-tickets/{tid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], tid)
    
    # Get (GET: /service-tickets/{id} => Not found)
    def test_get_ticket_not_found(self):
        response = self.client.get(f'/service-tickets/9999')
        self.assertEqual(response.status_code, 404)

    # Update (PUT: /service-tickets/{id})
    def test_update_ticket(self):
        create_customer = self.client.post("/customers/", json = {"name": "C", "email": "c@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]
        create_ticket = self.client.post(f"/service-tickets/", json = {"description": "Chirp", "customer_id": cid, "status": "open"})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]
        
        response = self.client.put(f"/service-tickets/{tid}", json = {"description": "Updated Chirp", "status": "closed"})
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["description"], "Updated Chirp")
        self.assertEqual(body["status"], "closed")
    
    # Update (PUT: /service-tickets/{id} -> Not found)
    def test_update_ticket_not_found(self):
        response = self.client.put(f'/service-tickets/9999', json = {"status": "closed"})
        self.assertEqual(response.status_code, 404)
    
    # Delete attempt (DELETE: /service-tickets/{id})
    def test_delete_ticket(self):
        create_customer = self.client.post("/customers/", json = {"name": "D", "email": "d@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]
        create_ticket = self.client.post("/service-tickets/", json = {"description": "Delete", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]
        
        response = self.client.delete(f"/service-tickets/{tid}")
        self.assertEqual(response.status_code, 200)
    
    # Delete attempt (DELETE: /service-tickets/{id} -> Not Found)
    def test_delete_not_found(self):
        response = self.client.delete(f'/service-tickets/9999')
        self.assertEqual(response.status_code, 404)

    # Assign Mechanic
    def test_assign_mechanic_to_ticket(self):
        create_customer = self.client.post("/customers/", json = {"name": "E", "email": "e@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]

        create_ticket = self.client.post("/service-tickets/", json = {"description": "Assign", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]
        
        create_mechanic = self.client.post("/mechanics/", json = {"name": "Alex", "email": "alex@shop.com"})
        self.assertEqual(create_mechanic.status_code, 201)
        mid = create_mechanic.get_json()["id"]
        
        response = self.client.put(f"/service-tickets/{tid}/assign-mechanic/{mid}")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(any(mech["id"] == mid for mech in body ["mechanics"]))

    #  Remove Mechanic
    def test_remove_mechanic_from_ticket(self):
        create_customer = self.client.post("/customers/", json = {"name": "F", "email": "f@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]
        
        create_ticket = self.client.post("/service-tickets/", json = {"description": "Assign", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]
        
        create_mechanic = self.client.post("/mechanics/", json = {"name": "Jane", "email": "jane@shop.com"})
        self.assertEqual(create_mechanic.status_code, 201)
        mid = create_mechanic.get_json()["id"]

        # Assign
        assign = self.client.put(f"/service-tickets/{tid}/assign-mechanic/{mid}")
        self.assertEqual(assign.status_code, 200)
        
        # Remove
        response = self.client.put(f"/service-tickets/{tid}/remove-mechanic/{mid}")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertFalse(any(mech["id"] == mid for mech in body["mechanics"]))

    # Bulk Edit Mechanics
    def test_bulk_edit_mechanics(self):
        create_customer = self.client.post("/customers/", json = {"name": "G", "email": "g@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]

        create_ticket = self.client.post("/service-tickets/", json = {"description": "Bulk", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]

        mechanic1 = self.client.post("/mechanics/", json = {"name": "Justine", "email": "justine@shop.com"})
        self.assertEqual(mechanic1.status_code, 201)
        id1 = mechanic1.get_json()["id"]

        mechanic2 = self.client.post("/mechanics/", json = {"name": "Patrick", "email": "patrick@shop.com"})
        self.assertEqual(mechanic2.status_code, 201)
        id2 = mechanic2.get_json()["id"]

        # add both
        add_response = self.client.put(f"/service-tickets/{tid}/edit", json = {"add_mechanics": [id1, id2], "remove_mechanics": []})
        self.assertEqual(add_response.status_code, 200)
        self.assertEqual({m["id"] for m in add_response.get_json()["mechanics"]}, {id1, id2})

        # remove one
        remove_response = self.client.put(f"/service-tickets/{tid}/edit", json = {"add_mechanics": [], "remove_mechanics": [id1]})
        self.assertEqual(remove_response.status_code, 200)
        self.assertEqual({m["id"] for m in remove_response.get_json()["mechanics"]}, {id2})

    def test_add_part_to_ticket(self):
        create_customer = self.client.post("/customers/", json = {"name": "H", "email": "h@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]
        
        create_ticket = self.client.post("/service-tickets/", json = {"description": "Add Part", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]
        
        create_part = self.client.post("/inventory/", json = {"name": "Rotor", "price": 79.50})
        self.assertEqual(create_part.status_code, 201)
        pid = create_part.get_json()["id"]
        
        response = self.client.post(f"/service-tickets/{tid}/add-part", json = {"part_id": pid})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(part["id"] == pid for part in response.get_json()["parts"]))

    def test_add_part_not_found(self):
        # Bad Ticket ID
        response1 = self.client.post("/service-tickets/9999/add-part", json = {"part_id": 1})
        self.assertEqual(response1.status_code, 404)

        # Good Ticket, Bad Part ID
        create_customer = self.client.post("/customers/", json = {"name": "I", "email": "i@sample.com", "password": "pass123"})
        self.assertEqual(create_customer.status_code, 201)
        cid = create_customer.get_json()["id"]

        create_ticket = self.client.post("/service-tickets/", json = {"description": "Bad Part", "customer_id": cid})
        self.assertEqual(create_ticket.status_code, 201)
        tid = create_ticket.get_json()["id"]

        response2 = self.client.post(f"/service-tickets/{tid}/add-part", json = {"part_id": 9999})
        self.assertEqual(response2.status_code, 404)