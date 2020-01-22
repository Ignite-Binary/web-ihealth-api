import json
import copy
from flask_migrate import stamp, upgrade
from flask_testing import TestCase
from app import db, create_app, redis_client
from api.models.users_model import User
from api.models.roles_model import Role
from fixtures.user_fixtures import user_1, user_2, admin_user, user_login
from fixtures.roles_fixtures import role_admin, role_patient, other_role


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = create_app('testing')
        self.headers = {'content-type': 'application/json'}
        self.patient_header = copy.deepcopy(self.headers)
        self.patient_refresh = copy.deepcopy(self.headers)
        self.admin_header = copy.deepcopy(self.headers)
        app.config['REDIS_URL'] = 'redis://localhost:6379/1'
        return app

    def setUp(self):
        app = self.create_app()
        self.app_client = app.test_client()
        with app.app_context():
            stamp(revision='base')
            upgrade()
            admin_role = Role(role_admin)
            admin_role.save()
            patient_role = Role(role_patient)
            patient_role.save()
            new_role = Role(other_role)
            new_role.save()
            user_admin = User(admin_user)
            user_admin.save()
            patient = User(user_1)
            patient.save()
            patient_2 = User(user_2)
            patient_2.save()
            db.session.commit()

    def tearDown(self):
        app = self.create_app()
        app.config['REDIS_URL'] = 'redis://localhost:6379/1'
        with app.app_context():
            db.session.remove()
            db.drop_all()
            redis_client.flushdb()


class CommonTestCases(BaseTestCase):
    """ common Tests"""
    def user_login(self):
        response = self.client.post(
            '/users/login',
            data=json.dumps(user_login), headers=self.headers)
        result = json.loads(response.data)
        self.patient_header['Authorization'] = f"Bearer {result['token']}"
        self.patient_refresh['Authorization'] = f"Bearer \
             {result['refresh']}"

    def admin_login(self):
        new_login = copy.deepcopy(user_login)
        new_login['user_name'] = 'john'
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.admin_header['Authorization'] = f"Bearer {result['token']}"
