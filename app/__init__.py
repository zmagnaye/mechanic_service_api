from flask import Flask
from app.extensions import ma
from app.models import db
from app.blueprints.mechanic import mechanic_bp
from app.blueprints.service_ticket import service_ticket_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")

    ma.init_app(app)
    db.init_app(app)

    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    return app