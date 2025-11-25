from app import create_app
from app.config import ProductionConfig
from app.models import db

#app = create_app("DevelopmentConfig")

app = create_app(ProductionConfig)


# with app.app_context():
#    db.create_all()
#
# app.run()