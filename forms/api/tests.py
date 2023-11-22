from django.test import TestCase
import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_forms(self):
        # Issue a GET request.
        response = self.client.get("/api/forms/")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_get_form(self):
        response = self.client.get("/api/get_form/?user_name=nik&user_email=mail.com")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 404)
