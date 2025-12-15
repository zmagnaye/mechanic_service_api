# Mechanic Service API

A RESTful API to manage customers, mechanics, service tickets, and inventory for a repair shop. Built with Flask, SQLAlchemy, and Marshmallow, following the application factory + blueprints pattern. Includes rate limiting, response caching, JWT token authentication, advanced relationship queries, and pagination. Fully documented with Swagger and tested using Python's unittest library. 

## Live Deployment

Base URL:
https://mechanic-service-api.onrender.com

Swagger Documentation:
https://mechanic-service-api.onrender.com/api/docs/

## Features

- Customer management (CRUD, login, my-tickets)
- Mechanic management (CRUD)
- Inventory management (CRUD)
- Service ticket management (CRUD, assign/remove mechanics, add parts, bulk edit)
- JWT token authentication for protected routes

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

Pipeline flow:
1. Build – Install dependencies
2. Test – Run all unit tests using unittest
3. Deploy – Automatically deploy to Render only if tests pass

Workflow file:
.github/workflows/main.yaml

## Tech Stack
- Python 3.x
- Flask, Flask-SQLAlchemy, Marshmallow, Flask-Marshmallow
- Flask-Limiter, Flask-Caching
- python-jose
- MySQL (mysql-connector)
- Swagger / Swagger-UI
- Unittest (for testing)

## Create Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

## Install dependencies
pip install -r requirements.txt

## Environment viriables:

Create a .env file in the project root with:

SECRET_KEY=your-secret-key
DATABASE_URL=your-production-database-url

Do not commit .env to GitHub.

## Run the app
python flask_app.py

## Run all unit tests
python -m unittest discover tests

## Testing

- Unit tests written using Python unittest
- Test configuration uses SQLite (TestingConfig)
- Tests are executed automatically in CI before deployment

## Authentication

- Login (/customers/login) returns a JWT with subject (sub) = customer_id
- Protected routes use @token_required and expect Authorization: Bearer <token>
- Token lifetime: 1 hour

## Rate Limiting & Caching

- Rate limiting via flask_limiter with a default limit and per-route limits (e.g., login: 5 per minute)
- Response caching via flask_caching (SimpleCache)

## Project Structure

mechanic_service_api/
├── app/
│   ├── blueprints/
│   ├── models/
│   ├── schemas/
│   ├── extensions.py
│   └── config.py
├── tests/
├── .github/workflows/
├── flask_app.py
├── requirements.txt
└── README.md

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

## Notes

- Built using Flask Application Factory pattern
- Blueprints used for modular API structure
- CI/CD pipeline prevents deployments if tests fail
- Designed for scalability and production use
