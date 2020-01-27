from flask_restplus import Namespace

user_ns = Namespace("users", description="users operations")
patient_prof_ns = Namespace("patients", description="patient profiles")
role_ns = Namespace("roles", description="user roles")
