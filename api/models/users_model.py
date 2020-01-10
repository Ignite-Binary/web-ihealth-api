from passlib.context import CryptContext
from flask_restplus import abort
from api.models.roles_model import Role
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
        return PASSLIB_CONTEXT.verify(password, self.password_hash)
