from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

class Base(DeclarativeBase):
    pass

db = SQLAlchemy()
ma = Marshmallow()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["200 per hour"]
)

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})