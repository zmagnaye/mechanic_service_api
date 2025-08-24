from app.extensions import ma
from marshmallow import Schema, fields
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class LoginSchema(Schema):
    email = fields.Str(required = True)
    password = fields.Str(required = True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many = True)
login_schema = LoginSchema()