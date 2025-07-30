import json
import urllib
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient

from djangoldp_uploader.models import File


class TestUPLOAD(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_uploaded(self):
        file_name = 'file.txt'
        file_url = '/upload/{}/{}'.format(get_random_string(32), file_name)
        sample_file = SimpleUploadedFile(file_name, b"file_content")

        response = self.client.put(file_url, {'file':sample_file})
        self.assertEqual(response.status_code, 201)

        response = self.client.get(file_url, follow=True)
        # self.assertEqual(response.status_code, 200)
        