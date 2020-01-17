from flask_restplus import Namespace

user_ns = Namespace("users", description="users operations")
role_ns = Namespace("roles", description="user roles")
