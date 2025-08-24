from flask import Flask
from app.config import Config
from app.extensions import ma, db, limiter, cache
from app.blueprints.mechanic import mechanic_bp
from app.blueprints.service_ticket import service_ticket_bp
from app.blueprints.customers import customer_bp
from app.blueprints.inventory import inventory_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")

    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    return app