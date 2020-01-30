from api.models.patient_profile_model import PatientProfile
from utitilies.database import db, Base


class DoctorProfile(Base):
    __tablename__ = 'doctor_profiles'
    patient_profile = db.Column(
        db.Integer, db.ForeignKey(PatientProfile.profile_user), nullable=False)
    specialty = db.Column(db.String(250), nullable=True)
    bio = db.Column(db.String(250), nullable=True)
    doctor_details = db.relationship('PatientProfile', uselist=False)
    # TODO: include doctor-facility relationship

    def __init__(self, profile):
        self.patient_profile = profile['patient_profile']
        self.specialty = profile.get('specialty')
        self.bio = profile.get('bio')

    def __repr__(self):
        return self.patient_profile
