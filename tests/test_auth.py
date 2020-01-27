import copy
import json
from tests.base import BaseTestCase, CommonTestCases
from fixtures.user_fixtures import user_login


class TestAuth(BaseTestCase):
    def test_user_login(self):
        response = self.client.post(
            '/users/login',
            data=json.dumps(user_login), headers=self.headers)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('token', str(result))

    def test_user_login_invalid_inputs(self):
        new_login = copy.deepcopy(user_login)
        new_login['status'] = 'active'
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('Unknown arguments', str(result))

    def test_login_unknown_user(self):
        new_login = copy.deepcopy(user_login)
        new_login['user_name'] = 'active'
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.assert401(response)
        self.assertIn('Invalid username or password!', str(result))

    def test_user_login_invalid_password(self):
        new_login = copy.deepcopy(user_login)
        new_login['password'] = 'active'
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.assert401(response)
        self.assertIn('Invalid username or password!', str(result))

    def test_refresh_token(self):
        CommonTestCases.patient_login(self)
        response = self.client.get(
            '/users/refresh', headers=self.patient_refresh)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('token', str(result))

    def test_logout(self):
        CommonTestCases.patient_login(self)
        response = self.client.delete(
            '/users/logout', headers=self.patient_header)
        self.assertStatus(response, 204)

    def test_logout_refresh(self):
        CommonTestCases.patient_login(self)
        response = self.client.delete(
            '/users/logout_refresh', headers=self.patient_refresh)
        self.assertStatus(response, 204)
