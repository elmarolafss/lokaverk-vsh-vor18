from late import db, app
from datetime import datetime

categories = ["dresses", "jackets", "tops", "jeans", "pants"]

def initialize_database():
    app.logger.info("Database is not created, exec create_all() here.")
    db.create_all()
    admin_user = User("admin","admin","admin")
    test_prod = Product(
            "lname",
            "name",
            4.2,
            "dresses",
            "col1$col2$col3",
            "/img1$/img2",
            "inf1$inf2$inf3",
            "s$m$l"
    )
    db.session.add(admin_user)
    db.session.add(test_prod)
    db.session.commit()

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
        return f"<User: {self.username}>"


class Product(db.Model):
    __tablename__ = "products"
    link_name = db.Column("lname", db.String(255), primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    price = db.Column(db.Float, index=True)
    category = db.Column(db.String(255), index=True)
    color = db.Column(db.String(255), index=True)
    colors = db.Column(db.String(255))
    images = db.Column(db.Text)
    info = db.Column(db.Text, index=True)
    sizes = db.Column(db.String(255))

    def __init__(self, ln, n, p, cat, cols, imgs, info, s):
        self.link_name = ln
        self.name = n
        self.price = p
        self.category = cat
        self.colors = cols
        self.color = self.make_array(self.colors)[0]
        self.images = imgs
        self.info = info
        self.sizes = s

    def __repr__(self):
        return self.name

    def make_array(self, str_arr, separator="$"):
        return str_arr.split(separator)

    def get_dict(self):
        return {
            "lname": self.link_name,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "color": self.color,
            "colors": self.make_array(self.colors),
            "images": self.make_array(self.images),
            "info": self.make_array(self.info),
            "sizes": self.make_array(self.sizes)
        }


class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column("purchase_id", db.Integer, primary_key=True)
    prod_name = db.Column(db.String(255), db.ForeignKey("products.lname"))
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
        self.used_id = uid
        self.discount = discount

    def __repr__(self):
        return self.id
