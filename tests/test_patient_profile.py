import json
from unittest.mock import patch
from tests.base import BaseTestCase, CommonTestCases
from fixtures.profile_fixtures import create_profile


class TestPatient(BaseTestCase):
    def test_create_patient_profile(self):
        CommonTestCases.patient_login(self)
        response = self.client.post(
            '/profiles/patients',
            data=json.dumps(create_profile), headers=self.patient_header)
        result = json.loads(response.data)
        self.assertStatus(response, 201)
        self.assertIn('profile_pic_3', str(result))

    def test_create_existing_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.post(
            '/profiles/patients',
            data=json.dumps(create_profile), headers=self.admin_header)
        result = json.loads(response.data)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('already exists', str(result))

    def test_create_patient_profile_without_pic(self):
        del create_profile['profile_pic']
        CommonTestCases.patient_login(self)
        response = self.client.post(
            '/profiles/patients',
            data=json.dumps(create_profile), headers=self.patient_header)
        result = json.loads(response.data)
        self.assertStatus(response, 201)
        self.assertIn('location', str(result))

    def test_fetch_all_patient_profiles(self):
        CommonTestCases.admin_login(self)
        response = self.client.get(
            '/profiles/patients', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('john', str(result))

    def test_fetch_patient_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.get(
            '/profiles/patients/1', headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('john', str(result))

    def test_patient_fetch_other_patient_profile(self):
        CommonTestCases.patient_login(self)
        response = self.client.get(
            '/profiles/patients/1', headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_update_patient_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.put(
            '/profiles/patients/1',
            data=json.dumps({"location": "mombasa Rd"}),
            headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('mombasa Rd', str(result))

    @patch('api.views.patient_profile_view.save_temp_image')
    def test_update_patient_profile_pic(self, saved_image):
        CommonTestCases.admin_login(self)
        saved_image.return_value = "profile_pic_1.jpg"
        response = self.client.put(
            '/profiles/patients/1',
            data=json.dumps({"profile_pic": "profile_pic_1.jpg"}),
            headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('profile_pic_1.jpg', str(result))

    def test_remove_profile_pic(self):
        CommonTestCases.admin_login(self)
        response = self.client.put(
            '/profiles/patients/1',
            data=json.dumps({"profile_pic": ""}),
            headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('user_profile.png', str(result))

    def test_update_profile_pic_unknown_name(self):
        CommonTestCases.admin_login(self)
        response = self.client.put(
            '/profiles/patients/1',
            data=json.dumps({"profile_pic": "prof.jpg"}),
            headers=self.admin_header)
        result = json.loads(response.data)
        self.assert200(response)
        self.assertIn('profile_pic_1.jpg', str(result))

    def test_patient_update_other_patient_profile(self):
        CommonTestCases.patient_login(self)
        response = self.client.put(
            '/profiles/patients/1',
            data=json.dumps({"last_name": "waiyaki"}),
            headers=self.patient_header)
        result = json.loads(response.data)
        self.assert403(response)
        self.assertIn('You are not authorized', str(result))

    def test_delete_patient_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.delete('/profiles/patients/3',
                                      headers=self.admin_header)
        self.assertStatus(response, 204)

    def test_delete_attached_patient_profile(self):
        CommonTestCases.admin_login(self)
        response = self.client.delete('/profiles/patients/4',
                                      headers=self.admin_header)
        result = json.loads(response.data)
        self.assert_403(response, 403)
        self.assertIn('cannot be deleted', str(result))
