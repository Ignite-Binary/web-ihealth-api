import json
import copy
from flask_migrate import stamp, upgrade
from flask_testing import TestCase
from app import db, create_app, redis_client
from api.models.users_model import User
from api.models.roles_model import Role
from api.models.patient_profile_model import PatientProfile
from api.models.doctor_profile_model import DoctorProfile
from fixtures.user_fixtures import (
    user_1, admin_user, test_doctor, doctor_user, doctor_user_2, user_login)
from fixtures.roles_fixtures import (
    role_admin, role_patient, role_doctor, other_role)
from fixtures.profile_fixtures import (
    patient_profile, doctor_profile, doc_patient_profile, admin_doc_profile,
    doc_patient_profile_2)


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = create_app('testing')
        self.headers = {'content-type': 'application/json'}
        self.patient_header = copy.deepcopy(self.headers)
        self.patient_refresh = copy.deepcopy(self.headers)
        self.admin_header = copy.deepcopy(self.headers)
        self.doctor_header = copy.deepcopy(self.headers)
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
            doctor_role = Role(role_doctor)
            doctor_role.save()
            new_role = Role(other_role)
            new_role.save()
            user_admin = User(admin_user)
            user_admin.save()
            admin_patient_profile = PatientProfile(patient_profile)
            admin_patient_profile.save()
            admin_doc = DoctorProfile(admin_doc_profile)
            admin_doc.save()
            patient = User(user_1)
            patient.save()
            test_doc = User(test_doctor)
            test_doc.save()
            test_doc_profile = PatientProfile(doc_patient_profile_2)
            test_doc_profile.save()
            user_doctor = User(doctor_user)
            user_doctor.save()
            doc_patient_prof = PatientProfile(doc_patient_profile)
            doc_patient_prof.save()
            doc_profile = DoctorProfile(doctor_profile)
            doc_profile.save()
            user_doctor_2 = User(doctor_user_2)
            user_doctor_2.save()
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

    def patient_login(self):
        response = self.client.post(
            '/users/login',
            data=json.dumps(user_login), headers=self.headers)
        result = json.loads(response.data)
        self.patient_header['Authorization'] = f"Bearer {result['token']}"
        self.patient_refresh['Authorization'] = f"Bearer \
             {result['refresh']}"

    def admin_login(self):
        new_login = {
            "user_name": "john",
            "password": "Abc123"
        }
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.admin_header['Authorization'] = f"Bearer {result['token']}"

    def doctor_login(self):
        new_login = {
            "user_name": "gideon",
            "password": "Abc123"
        }
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.doctor_header['Authorization'] = f"Bearer {result['token']}"
