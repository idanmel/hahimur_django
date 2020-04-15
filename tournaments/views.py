from django.http import JsonResponse
from .models import Token, Tournament, GroupMatchPrediction, KnockOutMatchPrediction, TopScorer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views import View


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
    return JsonResponse({"error": "Invalid token"}, status=404)


def get_user(request_token):
    return Token.objects.get(token=request_token).friend


class PredictionsView(View):
    def get(self, request, uid=1):
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

    def post(self, request, uid=1):
        request_token = request.GET.get('token')
        if not request_token:
            return no_token_error()

        try:
            user = get_user(request_token)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return invalid_token()

        return JsonResponse(PREDICTIONS)
