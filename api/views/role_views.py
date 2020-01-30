from flask_restplus import Resource
from helpers.roles_helper import role_validation, role_schema
from api.models.roles_model import Role as RoleModel
from api import user_ns
from utitilies.database import update_fields, db
from utitilies.auth import auth_user


role_schema = user_ns.model('Role', role_schema)


@user_ns.route('/roles')
class Roles(Resource):
    @auth_user(['admin'])
    @user_ns.marshal_list_with(role_schema, envelope='roles')
    def get(self):
        roles = RoleModel.query.all()
        return roles

    @auth_user(['admin'])
    @user_ns.expect(role_schema)
    @user_ns.marshal_with(role_schema, envelope='role')
    def post(self):
        role = role_validation()
        role_name = RoleModel.query.filter_by(
            role=role['role']).first()
        role_code = RoleModel.query.filter_by(
            code=role['code']).first()
        if role_name or role_code:
            try:
                existing_role = role_name.role
            except Exception:
                existing_role = role_code.code
            user_ns.abort(400, f"role {existing_role} already exists!")
        new_role = RoleModel(role)
        new_role.save()
        return new_role, 201


@user_ns.route('/roles/<int:role_id>')
class Role(Resource):
    @auth_user(['admin'])
    @user_ns.marshal_list_with(role_schema, envelope='role')
    def get(self, role_id):
        role = RoleModel.query.get_or_404(role_id, 'Role not Found')
        return role

    @auth_user(['admin'])
    @user_ns.expect(role_schema)
    @user_ns.marshal_with(role_schema, envelope='role')
    def put(self, role_id):
        role_updates = user_ns.payload
        role = RoleModel.query.get_or_404(role_id, 'Role not Found')
        role_validation(False)
        updated_role = update_fields(role, role_updates)
        try:
            updated_role.save()
        except Exception:
            db.session.rollback()
            user_ns.abort(403, f"role {role} code cannot be changed!")
        return updated_role

    @auth_user(['admin'])
    def delete(self, role_id):
        role = RoleModel.query.get_or_404(role_id, 'Role not Found')
        try:
            role.delete()
        except Exception:
            db.session.rollback()
            user_ns.abort(403, f"role {role} cannot be deleted!")
        return {"message": "role deleted"}, 204
