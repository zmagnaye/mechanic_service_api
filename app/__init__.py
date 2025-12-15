from flask import Flask
from app.config import Config
from app.extensions import ma, db, limiter, cache
from app.blueprints.mechanic import mechanic_bp
from app.blueprints.service_ticket import service_ticket_bp
from app.blueprints.customers import customer_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml" 
swaggerui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"appname": "Mechanic Service API"})

def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)
    #app.config.from_object(f"app.config.{config_name}")
    app.config.from_object(config_class)

    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    return app