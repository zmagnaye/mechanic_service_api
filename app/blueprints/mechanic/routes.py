from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanic_bp

# CREATE A MECHANIC
@mechanic_bp.route("/", methods = ["POST"])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
     
    mechanic = Mechanic(**data)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201

# GET ALL MECHANICS
@mechanic_bp.route("/", methods = ["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200

# GET A MECHANIC BY ID
@mechanic_bp.route("/<int:mechanic_id>", methods = ["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    return mechanic_schema.jsonify(mechanic), 200

# UPDATE A MECHANIC
@mechanic_bp.route("/<int:mechanic_id>", methods = ["PUT"])
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
@mechanic_bp.route("/<int:mechanic_id>", methods = ["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic) 
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} is deleted successfully."}), 200