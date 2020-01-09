from flask_restplus import Resource


class User(Resource):
    def get(self):
        return {'hello': 'user'}
