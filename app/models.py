from app import app, db
from datetime import datetime
import os.path

def initialize_database():
    if os.path.exists("./app.db"):
        return "Database already exists"
    app.logger.info("Database is not created, exec create_all() here.")
    db.create_all()
    admin_user = User("admin","admin","admin")
    db.session.add(admin_user)
    db.session.commit()
    return "Database created"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    joined = db.Column(db.DateTime)

    def __init__(self, uname, email, passw):
        self.username = uname
        self.email = email
        self.password_hash = passw
        self.joined = datetime.utcnow()

    def __repr__(self):
        return self.username

class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column("purchase_id", db.Integer, primary_key=True)
    prod_name = db.Column(db.String(255))
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"))
    price = db.Column(db.Float)
    size = db.Column(db.String(255))
    date = db.Column(db.DateTime)

    def __init__(self, pname, cid, price, size):
        self.prod_name = pname
        self.cart_id = cid
        self.price = price
        self.size = size
        self.date = datetime.utcnow()

    def __repr__(self):
        return f"item: {this.prod_name} added to cart: {cart_id}"


class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column("cart_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    total_pre_tax = db.Column(db.Float)
    discount = db.Column(db.Float)
    tax = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, uid, discount):
        self.user_id = uid
        self.discount = discount

    def __repr__(self):
        return self.id
