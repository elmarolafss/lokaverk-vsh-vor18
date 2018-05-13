import os
from flask import Flask

import click

from app.api import api_rest, api_bp
from app.client import client_bp
app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)

from .config import Config, flask_config
app.config.from_object(Config)
app.logger.info(">>> {}".format(flask_config))

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
