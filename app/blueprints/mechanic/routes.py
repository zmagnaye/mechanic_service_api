from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Mechanic
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from sqlalchemy import select

mechancis_bp = Blueprint("mechanics", __name__, url_prefix = "/mechnanics")

# CREATE A MECHANIC
@mechanics_bp.route("/", methods = ["POST"])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    mechanic = Mechanic(**data)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201

# GET ALL MECHANIC
@mechanics_bp.route("/", methods = ["GET"])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics)

# GET A MECHANIC BY ID
@mechanics_bp.route("/<int:mechanic_id>", methods = ["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    return mechanic_schema.jsonify(mechanic), 200

# UPDATE A MECHANIC
@mechanics_bp.route("/<int:mechanic_id>", methods = ["GET"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200
    
# DELETE MECHANIC
@mechanics_bp.route("/<int:mechanic_id>", methods = ["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic) 
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} is deleted successfully."}), 200