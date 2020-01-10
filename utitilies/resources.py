from flask_restplus import Api
from api.views.patients_view import user_ns

api = Api()
api.add_namespace(user_ns, path="/users")
