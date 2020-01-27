import copy
import json
from unittest.mock import patch
from tests.base import BaseTestCase, CommonTestCases
from fixtures.user_fixtures import create_user_1, user_1


class TestUser(BaseTestCase):
    @patch('api.views.users_view.user_validation')
    def test_user_signup(self, mock_user):
        mock_user.return_value = create_user_1
        print(create_user_1)
        response = self.client.post(
            '/users',
            data=json.dumps(create_user_1), headers=self.headers)
        result = json.loads(response.data)
        print(result)
        self.assertStatus(response, 201)
        self.assertIn('juma', str(result))

    @patch('api.views.users_view.user_validation')
    def test_sign_up_with_existing_username(self, mock_user):
        create_user = copy.deepcopy(create_user_1)
        create_user['user_name'] = user_1['user_name']
        mock_user.return_value = create_user
        response = self.client.post('/users', data=create_user)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    @patch('api.views.users_view.user_validation')
    def test_sign_up_with_existing_email(self, mock_user):
        create_user = copy.deepcopy(create_user_1)
        create_user['email'] = user_1['email']
        mock_user.return_value = create_user
        response = self.client.post('/users', data=create_user)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    def test_fetch_all_users(self):
        CommonTestCases.admin_login(self)
        response = self.client.get(
            '/users', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('peter', str(result))

    def test_fetch_specific_user(self):
        CommonTestCases.patient_login(self)
        response = self.client.get(
            '/users/2', headers=self.patient_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('peter', str(result))

    def test_patient_fetch_other_user(self):
        CommonTestCases.patient_login(self)
        response = self.client.get(
            '/users/3', headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_update_user(self):
        CommonTestCases.patient_login(self)
        response = self.client.put(
            '/users/2',
            data=json.dumps({"last_name": "waiyaki"}),
            headers=self.patient_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('waiyaki', str(result))

    def test_update_user_non_existing_role(self):
        CommonTestCases.patient_login(self)
        response = self.client.put(
            '/users/2',
            data=json.dumps({"role": 104}),
            headers=self.patient_header)
        result = json.loads(response.data)
        self.assert404(response)
        self.assertIn('Role not Found', str(result))

    def test_patient_update_other_user(self):
        CommonTestCases.patient_login(self)
        response = self.client.put(
            '/users/3',
            data=json.dumps({"last_name": "waiyaki"}),
            headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_delete_user(self):
        CommonTestCases.patient_login(self)
        response = self.client.delete('/users/2',
                                      headers=self.patient_header)
        self.assertStatus(response, 204)

    def test_patient_delete_other_user(self):
        CommonTestCases.patient_login(self)
        response = self.client.delete('/users/3',
                                      headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))
