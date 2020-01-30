from flask_restplus import Api
from api.views.users_view import user_ns
from api.views.role_views import user_ns as role_ns
from api.views.patient_profile_view import profiles_ns
from api.views.doctor_profile_view import profiles_ns as doc_profile_ns

api = Api()
api.add_namespace(user_ns, path="/users")
api.add_namespace(role_ns, path="/users")
api.add_namespace(profiles_ns, path="/profiles")
api.add_namespace(doc_profile_ns, path="/profiles")
