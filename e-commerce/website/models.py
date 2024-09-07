from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=3)
    role = db.relationship('Role', backref='users')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    discount = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=False)
    availability_status = db.Column(db.String(50), nullable=False)
    images = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(50), nullable=True)
    tag = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())