import json
from unittest.mock import patch
from tests.base import BaseTestCase
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
        response = self.client.get('/users/patients')
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('peter', str(result))

    def test_fetch_patient(self):
        response = self.client.get('/users/patients/1')
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('peter', str(result))

    def test_update_patient(self):
        response = self.client.put(
            '/users/patients/1',
            data=json.dumps({"last_name": "waiyaki"}), headers=self.headers)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('waiyaki', str(result))

    def test_delete_patient(self):
        response = self.client.delete('/users/patients/1')
        self.assertStatus(response, 204)
