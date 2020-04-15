from django.contrib.auth.models import User
from django.test import TestCase
from .models import Token, GroupMatchPrediction, Tournament, KnockOutMatchPrediction, TopScorer


class PredictionsViewTests(TestCase):
    """
    Testing the predictions URL.
    We are specifying the URL in the tests, because this guarantees usability to our frontend.
    """
    def setUp(self):
        self.t = Tournament.objects.create(name="Euro2020")

    def test_missing_token(self):
        """
        A request to a tournament without a token returns 401
        """
        response = self.client.get(f"http://127.0.0.1:8000/tournaments/{self.t.pk}/predictions")
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """
        A request to a tournament with an invalid token returns 403
        """
        response = self.client.get(f"http://127.0.0.1:8000/tournaments/{self.t.pk}/predictions?token=asd")
        self.assertEqual(response.status_code, 403)

    def test_valid_token(self):
        """
        A get request to with a valid token returns all predictions
        """
        test_user = User.objects.create_user(username='test', email='test@gmail.com', password='top_secret')
        Token.objects.create(token="vibrant-modric", friend=test_user)
        GroupMatchPrediction.objects.create(tournament=self.t, friend=test_user, match_number=1, home_score=3, away_score=2)
        GroupMatchPrediction.objects.create(tournament=self.t, friend=test_user, match_number=2, home_score=4, away_score=1)
        KnockOutMatchPrediction.objects.create(tournament=self.t, friend=test_user, match_number=3, home_score=0,
                                               away_score=1, home_win=False)
        TopScorer.objects.create(tournament=self.t, friend=test_user, name="Ronaldo")
        output = {
            "group_matches": [
                {"match_number": 1, "home_score": 3, "away_score": 2},
                {"match_number": 2, "home_score": 4, "away_score": 1},
            ],
            "knockout_matches": [{"match_number": 3, "home_score": 0, "away_score": 1, "home_win": False}],
            "top_scorer": "Ronaldo",
        }
        response = self.client.get(f"http://127.0.0.1:8000/tournaments/{self.t.pk}/predictions?token=vibrant-modric")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), output)

    def test_post_request(self):
        """
        A post request returns 200 and all the user predictions for a specific tournament
        """
        test_user = User.objects.create_user(username='test', email='test@gmail.com', password='top_secret')
        Token.objects.create(token="vibrant-modric", friend=test_user)
        data = {
            "group_matches": [
                {"match_number": 1, "home_score": 3, "away_score": 2},
                {"match_number": 2, "home_score": 4, "away_score": 1},
            ],
            "knockout_matches": [{"match_number": 3, "home_score": 0, "away_score": 1, "home_win": False}],
            "top_scorer": "Ronaldo",
        }
        response = self.client.post(f"http://127.0.0.1:8000/tournaments/{self.t.pk}/predictions?token=vibrant-modric",
                                    data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        group_match_predictions = GroupMatchPrediction.objects.filter(tournament=self.t).filter(friend=test_user)
        self.assertEqual(len(group_match_predictions), 2)

        ko_match_predictions = KnockOutMatchPrediction.objects.filter(tournament=self.t).filter(friend=test_user)
        self.assertEqual(len(ko_match_predictions), 1)

        top_scorer_name = TopScorer.objects.get(tournament=self.t, friend=test_user).name
        self.assertEqual(top_scorer_name, "ronaldo")


    def test_invalid_tournament(self):
        """
        An invalid tournament number returns 404
        """
        test_user = User.objects.create_user(username='test', email='test@gmail.com', password='top_secret')
        Token.objects.create(token="valid-token", friend=test_user)
        response = self.client.get(f"http://127.0.0.1:8000/tournaments/{self.t.pk + 1}/predictions?token=valid-token")
        self.assertEqual(response.status_code, 404)
