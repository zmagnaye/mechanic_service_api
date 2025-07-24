from app.extensions import db

ticket_mechanic = db.Table(
    "ticket_mechanic",
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_ticket.id")),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic_id"))
)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)

class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(300), nullable = False)
    status = db.Column(db.String(50), default = "open")
    mechanics = db.relationship("Mechanic", secondary = ticket_mechanic, backref = "tickets")