from django.test import TestCase
from django.urls import reverse


class PredictionsViewTests(TestCase):
    def test_missing_token(self):
        """
        A request to a tournament without a token, returns 401
        """
        response = self.client.get(reverse('tournaments:predictions', kwargs={'uid': 1}))
        self.assertEqual(response.status_code, 401)

    def test_bad_token(self):
        """
        A request to a tournament without a bad token, returns 403
        """
        response = self.client.get("http://127.0.0.1:8000/tournaments/1/predictions?token=asd")
        self.assertEqual(response.status_code, 403)
