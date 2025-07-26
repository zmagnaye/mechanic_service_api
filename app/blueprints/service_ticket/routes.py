from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, Mechanic, ticket_mechanic, db
from . import service_ticket_bp

# CREATE A TICKET
@service_ticket_bp.route("/", methods = ["POST"])
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
@service_ticket_bp.route("/", methods = ["GET"])
def get_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

# GET A TICKET BY ID
@service_ticket_bp.route("/<int:ticket_id>", methods = ["GET"])
def get_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    return service_ticket_schema.jsonify(ticket), 200

# UPDATE A TICKET
@service_ticket_bp.route("/<int:ticket_id>", methods = ["PUT"])
def update_ticket(ticket_id):
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
@service_ticket_bp.route("/<int:ticket_id>", methods = ["DELETE"])
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    db.session.delete(ticket) 
    db.session.commit()
    return jsonify({"message": f"Service ticket {ticket_id} is deleted successfully."}), 200

# ASSIGN SERVICE TICKET TO A MECHANIC
@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods = ["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

# REMOVES MECHANIC TO TICKET
@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods = ["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200