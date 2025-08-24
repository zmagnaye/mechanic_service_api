from datetime import datetime
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.extensions import db, Base

ticket_mechanic = db.Table(
    "ticket_mechanic",
    Base.metadata,
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_ticket.id")),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic.id"))
)

ticket_part = db.Table(
    "ticket_part",
    Base.metadata,
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_ticket.id")),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"))
)

class Mechanic(Base):
    __tablename__ = "mechanic"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary = ticket_mechanic, back_populates = "mechanics")

class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(back_populates="customer", cascade = "all, delete")

class ServiceTicket(Base):
    __tablename__ = "service_ticket"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(db.String(300), nullable=False)
    status: Mapped[str] = mapped_column(db.String(50), nullable = False, default = "open")

    customer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("customer.id"))
    customer: Mapped["Customer"] = db.relationship(back_populates = "tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary= ticket_mechanic, back_populates="tickets")
    parts: Mapped[List["Inventory"]] = db.relationship(secondary= ticket_part, back_populates = "tickets")

class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary= ticket_part, back_populates = "parts")