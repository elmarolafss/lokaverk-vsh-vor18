import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click

from app.api import api_rest, api_bp
from app.client import client_bp

app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)

from . import config
app.config.from_object(config.Config)
app.logger.info(f">>> {config.flask_config}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

