from flask_restplus import Api
from api.views.users_view import user_ns
from api.views.role_views import role_ns
from api.views.profiles_view import patient_prof_ns

api = Api()
api.add_namespace(user_ns, path="/users")
api.add_namespace(role_ns, path="/users/roles")
api.add_namespace(patient_prof_ns, path="/profiles/patients")
