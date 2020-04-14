from django.contrib.auth.models import User
from django.test import TestCase
from .models import Token


class PredictionsViewTests(TestCase):
    """
    Testing the predictions URL.
    We are specifying the URL in the tests, because this guarantees usability to our frontend.
    """
    def test_missing_token(self):
        """
        A request to a tournament without a token returns 401
        """
        response = self.client.get("http://127.0.0.1:8000/tournaments/predictions")
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """
        A request to a tournament with an invalid token returns 403
        """
        response = self.client.get("http://127.0.0.1:8000/tournaments/predictions?token=asd")
        self.assertEqual(response.status_code, 403)

    def test_valid_token(self):
        """
        A request to a tournament with a valid token returns 200
        """
        test_user = User.objects.create_user(username='test', email='test@gmail.com', password='top_secret')
        token = Token.objects.create(token="vibrant-modric", friend=test_user)
        response = self.client.get("http://127.0.0.1:8000/tournaments/predictions?token=vibrant-modric")
        self.assertEqual(response.status_code, 200)
        self.assertIn("predictions", response.json())
        self.assertIsInstance(response.json()["predictions"], list)

    def test_post_request(self):
        """
        A post request returns 200
        """
        test_user = User.objects.create_user(username='test', email='test@gmail.com', password='top_secret')
        token = Token.objects.create(token="vibrant-modric", friend=test_user)
        response = self.client.post("http://127.0.0.1:8000/tournaments/predictions?token=vibrant-modric")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json(), {"user": "test"})
