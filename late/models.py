from late import db
from datetime import datetime

categories = ["dresses", "jackets", "tops", "jeans", "pants"]

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(128), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	joined = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return f"<User: {self.username}>"

class Product(db.Model):
	link_name = db.Column(db.String(255), primary_key=True)
	name = db.Column(db.String(255), index=True, unique=True)
	price = db.Column(db.Float, index=True)
	discount = db.Column(db.Float)
	category = db.Column(db.String(255), index=True)
	color = db.Column(db.String(255), index=True)
	colors = db.Column(db.String(255), index=True)
	images = db.Column(db.String(255), index=True)
	info = db.Column(db.String(255), index=True)
	sizes = db.Column(db.String(255))

	def colors_object(self):
		return Color(self.colors)

	def make_arry(self, str_arr, delimiter):
		return str_arr.split(delimiter)

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.link_name

class Purchase(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	prod_name = db.Column(db.String(255), db.ForeignKey('product.link_name'))
	cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
	price = db.Column(db.Float, index=True)
	discount = db.Column(db.Float, index=True)
	color = db.Column(db.String(255), index=True)
	size = db.Column(db.String(255), index=True)
	date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return f"item: {this.prod_name} added to cart: {cart_id}"

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	total_pre_tax = db.Column(db.Float, index=True)
	discount = db.Column(db.Float, index=True)
	tax = db.Column(db.Float, index=True)
	total = db.Column(db.Float, index=True)
	color = db.Column(db.String(255), index=True)

	def __repr__(self):
		return self.id