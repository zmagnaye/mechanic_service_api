from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db, limiter, cache
from app.models import Customer, ServiceTicket
from .schemas import customer_schema, customers_schema, login_schema
from app.utils.util import encode_token, token_required
from . import customer_bp

# CREATE A CUSTOMER
@customer_bp.route("/", methods = ["POST"])
def create_customer():
    try:
        data = customer_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
     
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201

# GET CUSTOMERS (with pagination)
@customer_bp.route("/", methods = ["GET"])
@cache.cached(timeout = 60, query_string=True)
def get_customers():
    try: 
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit and offset must be integers."}), 404
    
    q = select(Customer).limit(limit).offset(offset)
    rows = db.session.execute(q).scalars().all()
    return customers_schema.jsonify(rows), 200

# UPDATE A CUSTOMER
@customer_bp.route("/<int:customer_id>", methods = ["PUT"])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    payload = request.json or {}

    for k, v in payload.items():
        if hasattr(customer, k):
            setattr(customer, k, v)
    db.session.commit()
    return customer_schema.jsonify(customer), 200

#  DELETE A CUSTOMER
@customer_bp.route("/<int:customer_id>", methods = ["DELETE"])
@token_required
def delete_customer(token_customer_id, customer_id):
    if token_customer_id != customer_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Deleted customer {customer_id}"}), 200

# LOGIN: Returns Token
@customer_bp.route("/login", methods = ["POST"])
@limiter.limit("5 per minute")
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    q = select(Customer).where(Customer.email == credentials["email"])
    user = db.session.execute(q).scalar_one_or_none()

    if user and user.password == credentials["password"]:
        token = encode_token(user.id)
        return jsonify({"status": "success", "auth_token": token}), 200
    
    return jsonify({"message": "Invalid Email or Password"}), 401

# Protected: View my tickets
@customer_bp.route("/my-tickets", methods = ["GET"])
@token_required
def my_tickets(customer_id):
    q = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    service_tickets = db.session.execute(q).scalars().all()
    from app.blueprints.service_ticket.schemas import service_tickets_schema
    return service_tickets_schema.jsonify(service_tickets), 200