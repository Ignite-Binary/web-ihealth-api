from flask_restplus import Api
from api.views.patients_view import user_ns
from api.views.role_views import role_ns

api = Api()
api.add_namespace(user_ns, path="/users")
api.add_namespace(role_ns, path="/users/roles")
