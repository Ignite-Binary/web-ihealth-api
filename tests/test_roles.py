import json
from tests.base import BaseTestCase, CommonTestCases
from fixtures.roles_fixtures import new_role


class TestRole(BaseTestCase):
    def test_create_role(self):
        CommonTestCases.admin_login(self)
        response = self.client.post(
            '/users/roles',
            data=json.dumps(new_role), headers=self.admin_header)
        result = json.loads(response.data)
        self.assertStatus(response, 201)
        self.assertIn('new', str(result))

    def test_create_role_existing_rolename(self):
        CommonTestCases.admin_login(self)
        new_role['role'] = "admin"
        response = self.client.post(
            '/users/roles',
            data=json.dumps(new_role), headers=self.admin_header)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    def test_create_role_existing_code(self):
        CommonTestCases.admin_login(self)
        new_role['code'] = 4
        response = self.client.post(
            '/users/roles',
            data=json.dumps(new_role), headers=self.admin_header)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    def test_fetch_all_roles(self):
        CommonTestCases.admin_login(self)
        response = self.client.get('/users/roles', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('admin', str(result))

    def test_fetch_role(self):
        CommonTestCases.admin_login(self)
        response = self.client.get('/users/roles/1', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('admin', str(result))

    def test_update_role(self):
        CommonTestCases.admin_login(self)
        response = self.client.put(
            '/users/roles/3',
            data=json.dumps({"role": "administrator"}),
            headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('administrator', str(result))

    def test_update_attached_role(self):
        CommonTestCases.admin_login(self)
        response = self.client.put(
            '/users/roles/2',
            data=json.dumps({"code": 20}), headers=self.admin_header)
        result = json.loads(response.data)
        self.assertStatus(response, 403)
        self.assertIn('code cannot be changed', str(result))

    def test_delete_role(self):
        CommonTestCases.admin_login(self)
        response = self.client.delete(
            '/users/roles/3', headers=self.admin_header)
        self.assertStatus(response, 204)

    def test_delete_attached_role(self):
        CommonTestCases.admin_login(self)
        response = self.client.delete(
            '/users/roles/2', headers=self.admin_header)
        result = json.loads(response.data)
        self.assertStatus(response, 403)
        self.assertIn('cannot be deleted', str(result))
