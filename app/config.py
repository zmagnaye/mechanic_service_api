class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345@localhost/mechanic_service_api'
    DEBUG = True

class TestingConfig:
    pass

class ProductionCOnfig:
    pass