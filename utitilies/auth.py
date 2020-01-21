from functools import wraps
from flask_restplus import abort
from utitilies.redis import redis_client
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, get_jwt_claims)

jwt = JWTManager()


def auth_user(allowed_users):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if claims['role'] not in allowed_users:
                abort(403, 'You are not authorized!')
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# override the error returned to the user if the
# user_loader_callback returns None. If you don't override
# this, # it will return a 401 status code with the JSON:
# {"msg": "Error loading the user <identity>"}.
# You can use # get_jwt_claims() here too if desired
@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    abort(404, 'Claiming user does not exist!')


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return redis_client.exists(jti)
