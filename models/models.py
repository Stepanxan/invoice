from app import db
from datetime import datetime


from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.id}>"

class Invoice(db.Model):
    __tablename__ = 'Invoice'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    type = db.Column(db.String(10), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='invoices')
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    delivery_charge = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"<Invoice {self.id}>"