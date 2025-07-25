class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345@localhost/mechanic_service_api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True