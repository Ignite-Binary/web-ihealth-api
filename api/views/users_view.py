from flask_restplus import Resource
from flask_jwt_extended import (
    get_jwt_identity, jwt_refresh_token_required, jwt_required, get_raw_jwt)
from api.models.users_model import User
from api import user_ns
from utitilies.redis import redis_client


class Login(Resource):
    def post(self):
        user_details = user_ns.payload
        if not (['user_name', 'password'] == [*user_details]):
            user_ns.abort(400, 'Invalid username or password!')
        user = User.query.filter_by(
            user_name=user_details['user_name'], status='active').first()
        if not user:
            user_ns.abort(401, 'Invalid username or password!')
        if not user.verify_password(user_details['password']):
            user_ns.abort(401, 'Invalid username or password!')
        return {"token": user.token, "refresh": user.refresh_token}, 200


class Refresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        user = User.query.filter_by(
            id=get_jwt_identity(),
            status='active').first_or_404('Claiming user does not exist!')
        return {"token": user.token, "refresh": user.refresh_token}, 200


class Logout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        redis_client.set(jti, jti)
        return "Successfully logged out", 204


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        redis_client.set(jti, jti)
        return "Successfully logged out", 204
