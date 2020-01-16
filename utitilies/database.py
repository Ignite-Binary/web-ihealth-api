from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Utility(object):

    def save(self):
        """Function for saving new objects"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Function for deleting objects"""
        db.session.delete(self)
        db.session.commit()


class Base(db.Model, Utility):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())


def update_fields(model, updates):
    """
    Function to update model fields
    :param model
    :param updates
    """
    for key, value in updates.items():
        setattr(model, key, value)
    return model
