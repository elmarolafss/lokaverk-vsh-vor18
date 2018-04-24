from flask import request, render_template, flash, redirect, url_for, send_from_directory
from late import app
from late.models import categories

@app.route("/")
def index():
	return render_template("pages/index.html", categories=categories)

@app.route("/search")
def search():
	cat = request.args.get("cat")
	title = cat if cat else "Search"
	return render_template("pages/search.html", title=cat, categories=categories)

@app.route("/test")
def test():
	return render_template("pages/test.html", title="Test", categories=categories)
