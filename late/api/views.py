from flask import request, render_template, flash, redirect, url_for, send_from_directory, jsonify
from late import app
from late.models import categories, initialize_database, Product

@app.route("/")
def index():
	return render_template("pages/index.html", categories=categories)

@app.route("/db-init")
def db_init():
    return initialize_database()

@app.route("/products/get", methods=["GET"])
def products_get():
    products = Product.query.all()
    products = [prod.get_dict() for prod in products]
    return jsonify(products)

@app.route("/search")
def search():
	cat = request.args.get("cat")
	title = cat if cat else "Search"
	return render_template("pages/search.html", title=cat, categories=categories)

@app.route("/test")
def test():
	return render_template("pages/test.html", title="Test", categories=categories)
