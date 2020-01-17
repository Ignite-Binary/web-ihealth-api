from sqlalchemy.exc import IntegrityError
from flask_restplus import Resource
from helpers.roles_helper import role_validation, role_schema
from api.models.roles_model import Role as RoleModel
from api import role_ns
from utitilies.database import update_fields, db


role_schema = role_ns.model('Role', role_schema)


@role_ns.route('')
class Roles(Resource):
    @role_ns.marshal_list_with(role_schema, envelope='roles')
    def get(self):
        roles = RoleModel.query.all()
        return roles

    @role_ns.expect(role_schema)
    @role_ns.marshal_with(role_schema, envelope='role')
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
            role_ns.abort(400, f"role {existing_role} already exists!")
        new_role = RoleModel(role)
        new_role.save()
        return new_role, 201


@role_ns.route('/<int:role_id>')
class Role(Resource):
    @role_ns.marshal_list_with(role_schema, envelope='role')
    def get(self, role_id):
        role = RoleModel.query.get_or_404(role_id, 'Role not Found')
        return role

    @role_ns.expect(role_schema)
    @role_ns.marshal_with(role_schema, envelope='role')
    def put(self, role_id):
        role_updates = role_ns.payload
        role = RoleModel.query.get_or_404(role_id, 'Role not Found')
        role_validation(False)
        updated_role = update_fields(role, role_updates)
        try:
            updated_role.save()
        except IntegrityError:
            db.session.rollback()
            role_ns.abort(403, f"role {role} code cannot be changed!")
        return updated_role

    def delete(self, role_id):
        role = RoleModel.query.get_or_404(role_id, 'Role not Found')
        try:
            role.delete()
        except IntegrityError:
            db.session.rollback()
            role_ns.abort(403, f"role {role} cannot be deleted!")
        return {"message": "role deleted"}, 204