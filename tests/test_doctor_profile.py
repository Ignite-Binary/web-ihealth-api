import json
from tests.base import BaseTestCase, CommonTestCases
from fixtures.profile_fixtures import create_doc_profile


class TestDoctor(BaseTestCase):
    def test_create_doctor_profile(self):
        new_login = {
            "user_name": "mary",
            "password": "Abc123"
        }
        response = self.client.post(
            '/users/login',
            data=json.dumps(new_login), headers=self.headers)
        result = json.loads(response.data)
        self.headers['Authorization'] = f"Bearer {result['token']}"

        response = self.client.post(
            '/profiles/doctors',
            data=json.dumps(create_doc_profile), headers=self.headers)
        result = json.loads(response.data)
        print(result)
        self.assertStatus(response, 201)
        self.assertIn('pathologist', str(result))

    def test_create_existing_doctor_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.post(
            '/profiles/doctors',
            data=json.dumps(create_doc_profile), headers=self.admin_header)
        result = json.loads(response.data)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    def test_fetch_all_doctor_profiles(self):
        CommonTestCases.admin_login(self)
        response = self.client.get(
            '/profiles/doctors', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('calli', str(result))

    def test_fetch_doctor_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.get(
            '/profiles/doctors/4', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('calli', str(result))

    def test_update_patient_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.put(
            '/profiles/doctors/4',
            data=json.dumps({"specialty": "pediatric"}),
            headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('pediatric', str(result))

    def test_doctor_update_other_doctor_profile(self):
        CommonTestCases.doctor_login(self)
        response = self.client.put(
            '/profiles/doctors/1',
            data=json.dumps({"specialty": "pediatric"}),
            headers=self.doctor_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_delete_doctor_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.delete('/profiles/doctors/4',
                                      headers=self.admin_header)
        self.assertStatus(response, 204)
