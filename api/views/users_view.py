import os
from werkzeug.datastructures import FileStorage
from flask_restplus import Resource, reqparse
from flask_jwt_extended import (
    get_raw_jwt, jwt_required, jwt_refresh_token_required,
    get_jwt_identity, current_user)
from api import user_ns
from utitilies.database import update_fields
from utitilies.auth import auth_user
from utitilies.redis import redis_client
from helpers.validators import user_validation
from helpers.users_helper import allowed_images, verify_owner
from api.models.users_model import User
from api.models.roles_model import Role
from api.models.schemas.user_schema import user_schema


user_schema = user_ns.model('User', user_schema)

upload_parser = user_ns.parser().add_argument('profile_pic', location='files',
                                              type=FileStorage, required=True,
                                              help="profile picture")


def login_parser():
    parser = user_ns.parser()
    parser.add_argument('user_name', type=str, trim=True,
                        help='Username', location='json')
    parser.add_argument('password', type=str, trim=True,
                        help='Password', location='json')
    return parser


@user_ns.route('')
class UsersView(Resource):
    @auth_user(['admin', 'facility_admin'])
    @user_ns.marshal_list_with(user_schema, envelope='users')
    def get(self):
        users = User.query.filter_by(status='active').all()
        return users

    @user_ns.expect(user_schema)
    @user_ns.marshal_with(user_schema, envelope='user')
    def post(self):
        user = user_validation(reqparse.RequestParser(
            trim=True, bundle_errors=True))
        user_name = User.query.filter_by(
            user_name=user['user_name'], status='active').first()
        user_email = User.query.filter_by(
            email=user['email'], status='active').first()
        if user_name or user_email:
            try:
                existing_user = user_name.user_name
            except Exception:
                existing_user = user_email.email
            user_ns.abort(400, f"{existing_user} already exists!")
        user['status'] = "active"
        user['role'] = 4
        new_user = User(user)
        new_user.save()
        return new_user, 201


@user_ns.route('/<int:user_id>')
class UserView(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @user_ns.marshal_with(user_schema, envelope='user')
    def get(self, user_id):
        user = User.query.filter_by(
            id=user_id,
            status='active').first_or_404('User not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(user.id, current_user.id)
        return user

    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @user_ns.expect(user_schema)
    @user_ns.marshal_with(user_schema, envelope='user')
    def put(self, user_id):
        user_updates = user_ns.payload
        user = User.query.filter_by(
            id=user_id,
            status='active').first_or_404('User not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(user.id, current_user.id)
        user_validation(reqparse.RequestParser(
            trim=True, bundle_errors=True), False)
        role_update = user_updates.get('role')
        if role_update:
            Role.query.filter_by(
                code=role_update).first_or_404('Role not Found')
        updated_user = update_fields(user, user_updates)
        updated_user.save()
        return updated_user

    @auth_user(['admin', 'patient'])
    def delete(self, user_id):
        user = User.query.filter_by(
            id=user_id,
            status='active').first_or_404('User not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(user.id, current_user.id)
        user.status = 'deleted'
        user.save()
        return {"message": "user deleted"}, 204


@user_ns.route('/profile_pic/<int:user_id>')
class PicUpload(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @user_ns.expect(upload_parser)
    def post(self, user_id):
        user = User.query.filter_by(
            id=user_id,
            status='active').first_or_404('User not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(user.id, current_user.id)
        uploaded_pic = upload_parser.parse_args()['profile_pic']
        file_type = allowed_images(uploaded_pic.filename)
        if not file_type:
            user_ns.abort(400, 'upload png, jpg/jpeg images!')
        new_file_name = f'profile_pic_{user.id}.{file_type}'
        uploaded_pic.save(os.path.join('static/temporary', new_file_name))
        return {'profile_pic': new_file_name}, 201


@user_ns.route('/login')
class Login(Resource):
    @user_ns.expect(login_parser())
    def post(self):
        user_details = login_parser().parse_args(strict=True)
        user = User.query.filter_by(
            user_name=user_details['user_name'], status='active').first()
        if not user:
            user_ns.abort(401, 'Invalid username or password!')
        if not user.verify_password(user_details['password']):
            user_ns.abort(401, 'Invalid username or password!')
        return {"token": user.token, "refresh": user.refresh_token}, 200


@user_ns.route('/refresh')
class Refresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        user = User.query.filter_by(
            id=get_jwt_identity(),
            status='active').first_or_404('Claiming user does not exist!')
        return {"token": user.token, "refresh": user.refresh_token}, 200


@user_ns.route('/logout')
class Logout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        redis_client.set(jti, jti)
        return "Successfully logged out", 204


@user_ns.route('/logout_refresh')
class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        redis_client.set(jti, jti)
        return "Successfully logged out", 204
