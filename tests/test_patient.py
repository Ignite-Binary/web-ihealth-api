import json
from unittest.mock import patch
from tests.base import BaseTestCase, CommonTestCases
from fixtures.user_fixtures import create_user_1, user_1


class TestPatient(BaseTestCase):
    @patch('api.views.patients_view.user_validation')
    def test_create_patient(self, mock_patient):
        mock_patient.return_value = create_user_1
        response = self.client.post(
            '/users/patients',
            data=json.dumps(create_user_1), headers=self.headers)
        result = json.loads(response.data)
        self.assertStatus(response, 201)
        self.assertIn('juma', str(result))

    @patch('api.views.patients_view.user_validation')
    def test_create_patient_existing_username(self, mock_patient):
        mock_patient.return_value = create_user_1
        create_user_1['user_name'] = user_1['user_name']
        response = self.client.post('/users/patients', data=create_user_1)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    @patch('api.views.patients_view.user_validation')
    def test_create_patient_existing_email(self, mock_patient):
        mock_patient.return_value = create_user_1
        create_user_1['email'] = user_1['email']
        response = self.client.post('/users/patients', data=create_user_1)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    def test_fetch_all_patients(self):
        CommonTestCases.admin_login(self)
        response = self.client.get(
            '/users/patients', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('peter', str(result))

    def test_fetch_patient(self):
        CommonTestCases.user_login(self)
        response = self.client.get(
            '/users/patients/2', headers=self.patient_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('peter', str(result))

    def test_patient_fetch_other_patient(self):
        CommonTestCases.user_login(self)
        response = self.client.get(
            '/users/patients/3', headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_update_patient(self):
        CommonTestCases.user_login(self)
        response = self.client.put(
            '/users/patients/2',
            data=json.dumps({"last_name": "waiyaki"}),
            headers=self.patient_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('waiyaki', str(result))

    def test_patient_update_other_patient(self):
        CommonTestCases.user_login(self)
        response = self.client.put(
            '/users/patients/3',
            data=json.dumps({"last_name": "waiyaki"}),
            headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_delete_patient(self):
        CommonTestCases.user_login(self)
        response = self.client.delete('/users/patients/2',
                                      headers=self.patient_header)
        self.assertStatus(response, 204)

    def test_patient_delete_other_patient(self):
        CommonTestCases.user_login(self)
        response = self.client.delete('/users/patients/3',
                                      headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))
