from flask import render_template, flash, redirect, url_for, send_from_directory
from late import app

@app.route("/")
def index():
  return render_template("index.html", title="Index")

@app.route("/test")
def test():
  return render_template("pages/test.html", title="Test")
