import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    ALG = "HS256" 


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345@localhost/mechanic_service_api'
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass

