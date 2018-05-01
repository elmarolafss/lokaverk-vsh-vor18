import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click

from late.api import api_rest, api_bp
from late.client import client_bp

app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import config
app.logger.info(f">>> {config.flask_config}")
