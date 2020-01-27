from api.models.users_model import User
from utitilies.database import db, Base


class PatientProfile(Base):
    __tablename__ = 'patient_profiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_user = db.Column(
        db.Integer, db.ForeignKey(User.id), nullable=False)
    profile_pic = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(250), nullable=True)
    state = db.Column(db.String(250), nullable=True)
    location = db.Column(db.String(250), nullable=True)
    user_details = db.relationship('User', uselist=False)

    def __init__(self, profile):
        self.profile_user = profile['user_id']
        self.profile_pic = profile['profile_pic']
        self.country = profile['country']
        self.state = profile['state']
        self.location = profile['location']

    def __repr__(self):
        return self.user_id

    @property
    def vitals(self):
        # TODO: fetch user vitals eg. height, weight and heart rate
        # from medical records
        pass
