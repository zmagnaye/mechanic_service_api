# Mechanic Service API

A RESTful API to manage customers, mechanics, service tickets, and inventory for a repair shop. Built with Flask, SQLAlchemy, and Marshmallow, following the application factory + blueprints pattern. Includes rate limiting, response caching, JWT token authentication, advanced relationship queries, and pagination.

## Features

- Flask blueprints & modular structure
- SQLAlchemy models with relationships (one-to-many & many-to-many)
- JWT token auth (python-jose)
- Rate limiting (Flask-Limiter): route-specific and default limits
- Response caching (Flask-Caching) with query-string support
- Advanced queries
  - Add/remove mechanics on a ticket (bulk edit route)
- Pagination on list endpoints (customers)
- Postman collection included

## Tech Stack
- Python 3.11+
- Flask, Flask-SQLAlchemy, Marshmallow, Flask-Marshmallow
- Flask-Limiter, Flask-Caching
- python-jose
- MySQL (mysql-connector)

## Authentication
- Login (/customers/login) returns a JWT with subject (sub) = customer_id
- Protected routes use @token_required and expect Authorization: Bearer <token>
- Token lifetime: 1 hour

## Rate Limiting & Caching
- Rate limiting via flask_limiter with a default limit and per-route limits (e.g., login: 5 per minute)
- Response caching via flask_caching (SimpleCache)

## Routes

### Mechanics (`/mechanics`)
- `POST /` – Create a new mechanic
- `GET /` – List all mechanics
- `GET /<id>` – Get mechanic by ID
- `PUT /<id>` – Update a mechanic
- `DELETE /<id>` – Delete a mechanic

### Service Tickets (`/service-tickets`)
- `POST /` – Create a new service ticket
- `GET /` – List all service tickets
- `GET /<id>` – Update a ticket
- `DELETE /<id>` – Delete a ticket
- `PUT /<ticket_id>` – Assign a mechanic
- `PUT /<ticket_id>/assign-mechanic/<mechanic_id>` – Assign a mechanic to a ticket
- `PUT /<ticket_id>/remove-mechanic/<mechanic_id>` – Remove a mechanic from a ticket
- `PUT /<ticket_id>/edit` – Add or remove multiple mechanics
- `POST /<ticket_id>/add-part` – Add an inventory part to a ticket

### Customers (`/customers`)
- `POST /` – Create a new customer
- `GET /` – List all customers (with pagination)
- `GET /` – View all tickets for the logged-in customer (Protected with JWT)
- `PUT /<id>` – Update a customer
- `DELETE /<id>` – Delete a customer (Protected with JWT)
- `POST /login` – Customer Login

### Inventory (`/inventory`)
- `POST /` – Create a new part
- `GET /` – List all parts
- `GET /<id>` – Get part by ID
- `PUT /<id>` – Update a part
- `DELETE /<id>` – Delete a part

## Testing
Use the included Postman collection:  
`Mechanic Service API.postman_collection.json`
