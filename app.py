from flask import Flask
from flask_restplus import Api
from config import config
from api.views.users import User

api = Api()

api.add_resource(User, '/users')


def create_app(obj_config):
    """create app"""
    app = Flask(__name__)
    app.config.from_object(config[obj_config])
    api.init_app(app)

    return app
