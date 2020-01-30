from api.models.users_model import User
from api.models.profiles_model import UserProfile
from utitilies.database import db, Base


class PatientProfile(Base, UserProfile):
    __tablename__ = 'patient_profiles'
    profile_user = db.Column(
        db.Integer, db.ForeignKey(User.id), unique=True, nullable=False)
    user_details = db.relationship('User', uselist=False)

    def __init__(self, profile):
        self.profile_user = profile.get('user_id')
        self.profile_pic = profile.get('profile_pic', '')
        self.country = profile.get('country', '')
        self.state = profile.get('state', '')
        self.location = profile.get('location', '')

    def __repr__(self):
        return self.profile_user

    @property
    def vitals(self):
        # TODO: fetch user vitals eg. height, weight and heart rate
        # from medical records
        pass
