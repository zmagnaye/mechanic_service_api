from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Customer
        email = ma.auto_field
        password = ma.auto_field

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many = True)
login_schema = LoginSchema()