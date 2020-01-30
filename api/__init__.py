from flask_restplus import Namespace

user_ns = Namespace("users", description="users operations")
profiles_ns = Namespace("profiles", description="profile operations")
