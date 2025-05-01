from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    from_location = db.relationship('Location', foreign_keys=[from_location_id])
    to_location = db.relationship('Location', foreign_keys=[to_location_id])
    product = db.relationship('Product')
