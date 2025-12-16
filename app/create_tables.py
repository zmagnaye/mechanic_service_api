from app import create_app
from app.extensions import db
from app.config import ProductionConfig

app = create_app(ProductionConfig)

with app.app_context():
    db.create_all()
    print("All tables created successfully.")