from late import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

categories = ["dresses", "jackets", "tops", "jeans", "pants"]

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(128), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	joined = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def set_hash(self, password_hash):
		self.password = generate_password_hash(password_hash)
		return password

	def check_hash(self, login_password):
		return check_password_hash(self.password, login_password)
	"""
	Dæmi:
	u = User(username="ornstrangesuxdix", password="password123")
	u.set_hash(password)
	u.check_hash(anotherpassword)
	>False
	u.check_hash(password)
	>True
	"""

	def __repr__(self):
		return f"<User: {self.username}>"

class Product(db.Model):
	link_name = db.Column(db.String(255), primary_key=True)
	name = db.Column(db.String(255), index=True, unique=True)
	price = db.Column(db.Float, index=True)
	discount = db.Column(db.Float)
	category = db.Column(db.String(255), index=True)
	color = db.Column(db.String(255), index=True)
	colors = db.Column(db.String(255))
	images = db.Column(db.Text)
	info = db.Column(db.Text, index=True)
	sizes = db.Column(db.String(255))

	def colors_object(self):
		return Color(self.colors)

	def make_array(self, str_arr, separator="$"):
		return str_arr.split(separator)

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.link_name

class Purchase(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	prod_name = db.Column(db.String(255), db.ForeignKey('product.link_name'))
	cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
	price = db.Column(db.Float)
	discount = db.Column(db.Float)
	color = db.Column(db.String(255))
	size = db.Column(db.String(255))
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"item: {this.prod_name} added to cart: {cart_id}"

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	total_pre_tax = db.Column(db.Float)
	discount = db.Column(db.Float)
	tax = db.Column(db.Float)
	total = db.Column(db.Float)
	color = db.Column(db.String(255))

	def __repr__(self):
		return self.id
