from app import create_app, db
from config import ProductionConfig

app = create_app(ProductionConfig)

with app.app_context():
    db.create_all()
    print("All tables created successfully.")