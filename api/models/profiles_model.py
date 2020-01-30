from utitilies.database import db


class UserProfile(object):
    profile_pic = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(250), nullable=True)
    state = db.Column(db.String(250), nullable=True)
    location = db.Column(db.String(250), nullable=True)
