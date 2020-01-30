from flask_restplus import Namespace

user_ns = Namespace("users", description="users operations")
profiles_ns = Namespace("profiles", description="profile operations")
patient_prof_ns = Namespace("patients", description="patient profiles")
role_ns = Namespace("roles", description="user roles")
facility_ns = Namespace("facilities", description="facilities")
