from flask import Flask
from config import config
from utitilies.database import db
from utitilies.resources import api
from utitilies.migrations import migrate
from utitilies.auth import jwt
from utitilies.redis import redis_client


def create_app(obj_config):
    """create app"""
    app = Flask(__name__)
    app.config.from_object(config[obj_config])
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
    jwt.init_app(app)
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)

    return app
