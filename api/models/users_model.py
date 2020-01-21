import datetime
from passlib.context import CryptContext
from flask_restplus import abort
from flask_jwt_extended import (
    create_access_token, get_jwt_claims, create_refresh_token)
from api.models.roles_model import Role
from utitilies.auth import jwt
from utitilies.database import db, Base
from utitilies.types import StatusType, GenderType


PASSLIB_CONTEXT = CryptContext(
    # in a new application with no previous schemes, start with pbkdf2 SHA512
    schemes=["pbkdf2_sha512"],
    deprecated="auto",
)


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(250), unique=True, nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.Enum(GenderType),
                       default=GenderType.male, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone_no = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250))
    _password = db.Column("password", db.Text)
    role = db.Column(db.Integer, db.ForeignKey(Role.code), nullable=False)
    status = db.Column(db.Enum(StatusType),
                       default=StatusType.active, nullable=False)
    user_role = db.relationship('Role', uselist=False)

    def __init__(self, user):
        self.user_name = user['user_name']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.gender = user['gender']
        self.dob = user['dob']
        self.phone_no = user['phone_no']
        self.email = user['email']
        self.password = user['password']
        self.role = user['role']
        self.status = 'active'

    def __repr__(self):
        return self.user_name

    @property
    def password(self):
        abort(403, "password is write-only")

    @password.setter
    def password(self, password):
        self._password = PASSLIB_CONTEXT.hash(password.encode("utf8"))

    def verify_password(self, password):
        return PASSLIB_CONTEXT.verify(password, self._password)

    # a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what custom claims
    # should be added to the access token.
    @jwt.user_claims_loader
    def add_claims_to_access_token(self):
        payload = {'role': self.user_role.role}
        return payload

    # a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what the identity
    # of the access token should be.
    @jwt.user_identity_loader
    def user_identity_lookup(self):
        return self.id

    @property
    def token(self):
        return create_access_token(self)

    @property
    def refresh_token(self):
        expires = datetime.timedelta(days=2)
        return create_refresh_token(self, expires_delta=expires)

    # This function is called whenever a protected endpoint is accessed,
    # and returns an object based on the tokens identity.
    # This is called after the token is verified. Note that this needs to
    # return None if the user could not be loaded for any reason,
    # such as not being found in the underlying data store
    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        claims = get_jwt_claims()
        if claims.get('role'):
            role = Role.query.filter_by(role=claims['role']).first()
            if not role:
                return None
            return User.query.filter_by(
                id=identity, role=role.code, status='active').first()
        return User.query.filter_by(
                id=identity, status='active').first()
