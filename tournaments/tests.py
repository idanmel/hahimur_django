from django.test import TestCase


class PredictionsViewTests(TestCase):
    def test_missing_token(self):
        """
        A request to a tournament without a token returns 401
        """
        response = self.client.get("http://127.0.0.1:8000/tournaments/1/predictions")
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """
        A request to a tournament with an invalid token returns 403
        """
        response = self.client.get("http://127.0.0.1:8000/tournaments/1/predictions?token=asd")
        self.assertEqual(response.status_code, 403)

    def test_valid_token(self):
        """
        A request to a tournament with a valid token returns 200
        """
        response = self.client.get("http://127.0.0.1:8000/tournaments/1/predictions?token=good_token")
        self.assertEqual(response.status_code, 200)
        self.assertIn("predictions", response.json())
        self.assertIsInstance(response.json()["predictions"], list)

    def test_post_request(self):
        """
        A post request returns 405
        """
        response = self.client.post("http://127.0.0.1:8000/tournaments/1/predictions")
        self.assertEqual(response.status_code, 405)
