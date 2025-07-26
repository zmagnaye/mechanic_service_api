# Mechanic Service API

A RESTful API to manage mechanics and service tickets for a repair shop. Built with Flask, SQLAlchemy, and Marshmallow.

## Features

- Full CRUD for Mechanics
- Service Ticket management
- Mechanic assignment/removal to/from tickets
- Modular architecture using Flask Blueprints
- Marshmallow for serialization
- Postman collection included

## Routes

### Mechanics (`/mechanics`)
- `POST /` – Create a new mechanic
- `GET /` – List all mechanics
- `PUT /<id>` – Update a mechanic
- `DELETE /<id>` – Delete a mechanic

### Service Tickets (`/service-tickets`)
- `POST /` – Create a new service ticket
- `GET /` – List all service tickets 
- `PUT /<ticket_id>/assign-mechanic/<mechanic_id>` – Assign a mechanic
- `PUT /<ticket_id>/remove-mechanic/<mechanic_id>` – Remove a mechanic

## Testing
Use the included Postman collection:  
`Mechanic Service API.postman_collection.json`
