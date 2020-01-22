from utitilies.database import db, Base


class Role(Base):
    __tablename__ = 'roles'
    role = db.Column(db.String(250), unique=True, nullable=False)
    code = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, role):
        self.role = role['role']
        self.code = role['code']

    def __repr__(self):
        return self.role
