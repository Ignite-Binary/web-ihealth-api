from flask_testing import TestCase
from app import db, create_app
from api.models.users_model import User
from api.models.roles_model import Role
from fixtures.user_fixtures import user_1
from fixtures.roles_fixtures import role_admin, role_patient, other_role


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = create_app('testing')
        self.headers = {'content-type': 'application/json'}
        return app

    def setUp(self):
        app = self.create_app()
        self.app_client = app.test_client()
        with app.app_context():
            db.create_all()
            admin_role = Role(role_admin)
            admin_role.save()
            patient_role = Role(role_patient)
            patient_role.save()
            new_role = Role(other_role)
            new_role.save()
            patient = User(user_1)
            patient.save()
            db.session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()
