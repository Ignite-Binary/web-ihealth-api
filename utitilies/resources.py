from flask_restplus import Api
from api.views.patients_view import user_ns
from api.views.role_views import role_ns
from api.views.users_view import Login, Refresh, Logout, LogoutRefresh

api = Api()
user_ns.add_resource(Login, '/login')
user_ns.add_resource(Refresh, '/refresh')
user_ns.add_resource(Logout, '/logout')
user_ns.add_resource(LogoutRefresh, '/logout_refresh')
api.add_namespace(user_ns, path="/users")
api.add_namespace(role_ns, path="/users/roles")
