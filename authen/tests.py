from rest_framework.response import Response

from django.test import TestCase
from django.test.client import Client

from authen.models import TGOwner, TGUser
from authen.views import OwnerViewSet


class ViewTest(TestCase):
    @staticmethod
    def get_test_data_create_view():
        return (
            "/api/owners/",
            {"user_id": 111, "username": "JohnCerlik"},
            {"username": "JohnCerlik", "user_id": 111, "first_name": "", "last_name": ""}
        )
    def test_create_view(self):
        test_path, test_data, test_correct_data = self.get_test_data_create_view()
        
        client = Client()
        response: Response = client.post(path=test_path, data=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, test_correct_data)
        