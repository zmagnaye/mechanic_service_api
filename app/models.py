from datetime import datetime
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.extensions import db

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

ticket_mechanic = db.Table(
    "ticket_mechanic",
    Base.metadata,
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_ticket.id")),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic.id"))
)

class Mechanic(Base):
    __tablename__ = "mechanic"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary = ticket_mechanic, back_populates = "mechanics")

class ServiceTicket(Base):
    __tablename__ = "service_ticket"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(db.String(300), nullable=False)
    status: Mapped[str] = mapped_column(default = "open")

    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary= ticket_mechanic, back_populates="tickets")