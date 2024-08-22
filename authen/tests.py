from rest_framework.response import Response

from django.test import TestCase
from django.test.client import Client

from authen.models import TGOwner, TGUser
from authen.views import OwnerViewSet


class ViewTest(TestCase):
    @staticmethod
    def get_test_data_create_view():
        return (
            "/api/owners/create/",
            {"user_id": 111, "username": "JohnCerlik", "password": 1234, "last_name": "Cerlik"},
            {"username": "JohnCerlik", "user_id": 111, "first_name": "", "last_name": "Cerlik"}
        )
    @staticmethod
    def get_test_data_retrieve_view():
        return (
            "/api/owners/",
            {"user_id": 111, "passwrod": 111},
            {"username": "JohnCerlik", "user_id": 111, "first_name": "", "last_name": "Cerlik"}
        )
    @staticmethod
    def get_test_data_patch_view():
        return (
            "/api/owners/",
            {"User-Id": 111, "User-Password": 111},
            {"first_name": "John", "last_name": "Cerlik", "language": "ru", "city": "Dubna"},
            {"user_id": 111, "username": "JohnCerlik", "user_id": 111, "first_name": "John", "last_name": "Cerlik", "language": "ru", "city": "Dubna", "lat": None, "lon": None}
        )

    def test_create_view(self):
        test_path, test_data, test_correct_data = self.get_test_data_create_view()
        
        client = Client()
        response: Response = client.post(path=test_path, data=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, test_correct_data)

    def test_retrieve_view(self):
        create_path, create_data, _ = self.get_test_data_create_view()
        retrieve_path, retrieve_headers, correct_data = self.get_test_data_retrieve_view()

        client = Client()
        client.post(path=create_path, data=create_data)
        response: Response = client.get(retrieve_path, headers=retrieve_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], correct_data["first_name"])
        self.assertEqual(response.data["last_name"], correct_data["last_name"])

    def test_patch_view(self):
        create_path, create_data, _ = self.get_test_data_create_view()
        patch_path, patch_headers, patch_data, correct_data = self.get_test_data_patch_view()

        client = Client()
        client.post(path=create_path, data=create_data)
        response: Response = client.patch(path=patch_path, headers=patch_headers, data=patch_data, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        print(response.data)
        self.assertDictEqual(response.data, correct_data)
