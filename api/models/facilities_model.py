from passlib.context import CryptContext
from utitilies.database import db, Base
from utitilies.types import StatusType

PASSLIB_CONTEXT = CryptContext(
    # in a new application with no previous schemes, start with pbkdf2 SHA512
    schemes=["pbkdf2_sha512"],
    deprecated="auto",
)


class Facility(Base):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    certifications = db.Column(db.String(250), nullable=False)
    phoneNo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Enum(StatusType),
                       default=StatusType.active, nullable=False)

    def __init__(self, facility):
        self.name = facility['name']
        self.location = facility['location']
        self.certifications = facility['certifications']
        self.phoneNo = facility['phoneNo']
        self.email = facility['email']
        self.status = 'active'

    def __repr__(self):
        return self.facility
