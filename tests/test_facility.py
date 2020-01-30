import json
from unittest.mock import patch
from tests.base import BaseTestCase
from fixtures.facility_fixtures import create_facility_1, facility_1


class TestFacility(BaseTestCase):
    @patch('api.views.facilities_view.facility_validation')
    def test_create_facility(self, mock_facility):
        mock_facility.return_value = create_facility_1
        response = self.client.post(
            '/facilities',
            data=json.dumps(create_facility_1), headers=self.headers)
        result = json.loads(response.data)
        print(response.data)
        self.assertStatus(response, 201)
        self.assertIn('', str(result))

    @patch('api.views.facilities_view.facility_validation')
    def test_create_facility_existing_email(self, mock_facility):
        mock_facility.return_value = create_facility_1
        create_facility_1['email'] = facility_1['email']
        response = self.client.post('/facilities', data=create_facility_1)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('', str(result))

    def test_fetch_all_facilities(self):
        response = self.client.get('/facilities/1')
        result = json.loads(response.data)
        print(response.data)
        self.assert200(response)
        self.assertIn('kilimani', str(result))

    def test_fetch_facility(self):
        response = self.client.get('/facilities/1')
        result = json.loads(response.data)
        print(response.data)
        self.assertStatus(response, 200)
        self.assertIn('kilimani', str(result))

    def test_update_facility(self):
        response = self.client.put(
            '/facilities/1',
            data=json.dumps({"name": "Kilimani"}), headers=self.headers)
        result = json.loads(response.data)
        print(response.data)
        self.assert200(response)
        self.assertIn('kilimani', str(result))

    def test_delete_facility(self):
        response = self.client.delete('/facilities/1')
        print(response.data)
        self.assertStatus(response, 204)
