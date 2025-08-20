from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db
from app.models import Inventory
from .schemas import inventory_schema, inventories_schema
from . import inventory_bp

# CREATE A PART
@inventory_bp.route("/", methods = ["POST"])
def create_part():
    try: 
        data = inventory_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    part = Inventory(**data)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201

# READ PART
@inventory_bp.route("/", methods = ["GET"])
def list_parts():
    rows = db.session.execute(select(Inventory)).scalars().all()
    return inventory_schema.jsonify(rows), 200

# GET A PART
@inventory_bp.route("/<int:part_id>", methods = ["GET"])
def get_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part: 
        return jsonify({"error": "Not found"}), 404

    return inventory_schema.jsonify(part), 200

# UPDATE A PART
@inventory_bp.route("/<int:part_id>", methods = ["PUT"])
def update_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part: 
        return jsonify({"error": "Not found"}), 404
    for k,v in (request.json or {}).items():
        if hasattr(part, k): 
            setattr(part, k, v)
    db.session.commit()
    return inventory_schema.jsonify(part), 200

# DELETE A PART
@inventory_bp.route("/<int:part_id>", methods = ["DELETE"])
def deelte_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part: 
        return jsonify({"error": "Not found"}), 404
    
    db.session.commit()
    return jsonify({"message": f"Deleted part {part_id}"}), 200