import json
import copy
from unittest.mock import patch
from tests.base import BaseTestCase, CommonTestCases
from fixtures.user_fixtures import image_upload, invalid_image


class TestFiles(BaseTestCase):
    @patch('api.views.users_view.FileStorage.save')
    def test_image_upload(self, mock_save):
        CommonTestCases.patient_login(self)
        upload_header = copy.deepcopy(self.patient_header)
        upload_header['content-type'] = "multipart/form-data"
        response = self.client.post(
            '/users/profile_pic/2',
            data=image_upload, headers=upload_header)
        result = json.loads(response.data)
        mock_save.assert_called_with("static/temporary/profile_pic_2.png")
        self.assertStatus(response, 201)
        self.assertIn('profile_pic_2.png', str(result))

    def test_upload_invalid_image(self):
        CommonTestCases.patient_login(self)
        upload_header = copy.deepcopy(self.patient_header)
        upload_header['content-type'] = "multipart/form-data"
        response = self.client.post(
            '/users/profile_pic/2',
            data=invalid_image, headers=upload_header)
        result = json.loads(response.data)
        self.assert400(response)
        self.assertIn('upload png', str(result))
