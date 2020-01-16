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
        self.assertStatus(response, 201)

    def test_create_patient_existing_username(self):
        create_user_1['user_name'] = user_1['user_name']
        response = self.client.post('/users/patients', data=create_user_1)
        self.assert400(response)

    def test_create_patient_existing_email(self):
        create_user_1['email'] = user_1['email']
        response = self.client.post('/users/patients', data=create_user_1)
        self.assert400(response)

    def test_fetch_all_patients(self):
        response = self.client.get('/users/patients')
        self.assert200(response)

    def test_fetch_patient(self):
        response = self.client.get('/users/patients/1')
        self.assert200(response)

    def test_update_patient(self):
        response = self.client.put(
            '/users/patients/1',
            data=json.dumps({"password": "A788ka"}), headers=self.headers)
        print(response.data)
        self.assert200(response)

    def test_delete_patient(self):
        response = self.client.delete('/users/patients/1')
        self.assertStatus(response, 204)
