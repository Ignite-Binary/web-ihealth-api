from flask import Flask
from config import config
from utitilies.database import db
from utitilies.resources import api
from utitilies.migrations import migrate


def create_app(obj_config):
    """create app"""
    app = Flask(__name__)
    app.config.from_object(config[obj_config])
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
