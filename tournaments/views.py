import json

from django.http import JsonResponse
from .models import Token, Tournament, GroupMatchPrediction, KnockOutMatchPrediction, TopScorer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views import View
from django.db.utils import IntegrityError


PREDICTIONS = {
    "group_matches": [],
    "knockout_matches": [],
    "top_scorer": "",
}


def serialize_group_match(ko_match):
    return {
        "match_number": ko_match.match_number,
        "home_score": ko_match.home_score,
        "away_score": ko_match.away_score,
    }


def serialize_knockout_match(ko_match):
    return {
        "match_number": ko_match.match_number,
        "home_score": ko_match.home_score,
        "away_score": ko_match.away_score,
        "home_win": ko_match.home_win,
    }


def no_token_error():
    return JsonResponse({"error": "No token"}, status=401)


def invalid_token():
    return JsonResponse({"error": "Invalid token"}, status=403)


def invalid_tournament():
    return JsonResponse({"error": "Invalid tournament"}, status=404)


def get_user(request_token):
    return Token.objects.get(token=request_token).friend


def create_group_match_prediction(t, user, match_dict):
    match_number = match_dict["match_number"]
    home_score = match_dict["home_score"]
    away_score = match_dict["away_score"]
    return GroupMatchPrediction(tournament=t, friend=user, match_number=match_number, home_score=home_score,
                                away_score=away_score)


def create_ko_match_prediction(t, user, match_dict):
    match_number = match_dict["match_number"]
    home_score = match_dict["home_score"]
    away_score = match_dict["away_score"]
    home_win = match_dict["home_win"]
    return KnockOutMatchPrediction(tournament=t, friend=user, match_number=match_number, home_score=home_score,
                                   away_score=away_score, home_win=home_win)


class PredictionsView(View):
    def get(self, request, uid):
        request_token = request.GET.get('token')
        if not request_token:
            return no_token_error()

        try:
            user = get_user(request_token)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Invalid token"}, status=403)

        try:
            t = Tournament.objects.get(pk=uid)
        except ObjectDoesNotExist:
            return invalid_tournament()
        else:
            group_matches = GroupMatchPrediction.objects.filter(tournament=t).filter(friend=user)
            serialized_group_matches = [serialize_group_match(match) for match in group_matches]

            ko_matches = KnockOutMatchPrediction.objects.filter(tournament=t).filter(friend=user)
            serialized_knockout_matches = [serialize_knockout_match(match) for match in ko_matches]

            q = TopScorer.objects.get(tournament=t, friend=user)
            output = {
                "group_matches": serialized_group_matches,
                "knockout_matches": serialized_knockout_matches,
                "top_scorer": q.name,
            }

        return JsonResponse(output)

    def post(self, request, uid):
        request_token = request.GET.get('token')
        if not request_token:
            return no_token_error()

        try:
            user = get_user(request_token)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return invalid_token()

        try:
            t = Tournament.objects.get(pk=uid)
        except ObjectDoesNotExist:
            return invalid_tournament()

        data = json.loads(request.body.decode("utf-8"))
        for group_match_prediction in data["group_matches"]:
            GroupMatchPrediction.objects.update_or_create(
                tournament=t,
                friend=user,
                match_number=group_match_prediction["match_number"],
                home_score=group_match_prediction["home_score"],
                away_score=group_match_prediction["away_score"],
            )

        for ko_match_prediction in data["knockout_matches"]:
            KnockOutMatchPrediction.objects.update_or_create(
                tournament=t,
                friend=user,
                match_number=ko_match_prediction["match_number"],
                home_score=ko_match_prediction["home_score"],
                away_score=ko_match_prediction["away_score"],
                home_win=ko_match_prediction["home_win"]
            )

        top_scorer = data["top_scorer"].strip().lower()
        TopScorer.objects.update_or_create(tournament=t, friend=user, name=top_scorer)

        return JsonResponse({"success": "Predictions saved"})
