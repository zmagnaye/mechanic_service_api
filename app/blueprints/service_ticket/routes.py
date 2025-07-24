from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import ServiceTicket
from app.blueprints.service_ticket.schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError
from sqlalchemy import select

tickets_bp = Blueprint("tickets", __name__, url_prefix = "/tickets")

# CREATE A TICKET
@tickets_bp.route("/", methods = ["POST"])
def create_ticket():
    try:
        data = service_ticket_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

# GET ALL TICKETS
@tickets_bp.route("/", methods = ["GET"])
def get_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

# GET A TICKET BY ID
@tickets_bp.route("/<int:ticket_id>", methods = ["GET"])
def get_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    return service_ticket_schema.jsonify(ticket), 200

# UPDATE A TICKET
@tickets_bp.route("/<int:tickets_id>", methods = ["PUT"])
def update_mechanic(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in data.items():
        setattr(ticket, key, value)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

# DELETE A TICKET
@tickets_bp.route("/<int:tickets_id>", methods = ["DELETE"])
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    db.session.delete(ticket) 
    db.session.commit()
    return jsonify({"message": f"Service ticket {ticket_id} is deleted successfully."}), 200