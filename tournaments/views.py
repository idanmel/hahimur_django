import json

from django.http import JsonResponse
from .models import Token, Tournament, GroupMatchPrediction, KnockOutMatchPrediction, TopScorer
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views import View


PREDICTIONS = {
    "group_matches": [],
    "knockout_matches": [],
    "top_scorer": "",
}


def get_user(request_token):
    return Token.objects.get(token=request_token).friend


class PredictionsView(View):
    def get(self, request, uid=1):
        request_token = request.GET.get('token')
        if not request_token:
            return JsonResponse({}, status=401)

        try:
            user = get_user(request_token)
            t = Tournament.objects.get(pk=uid)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=403)
        else:
            q = GroupMatchPrediction.objects.filter(tournament=t).filter(friend=user)
            data = serializers.serialize("json", q, fields=("match_number", "home_score", "away_score"))
            group_matches = [d["fields"] for d in json.loads(data)]

            q = KnockOutMatchPrediction.objects.filter(tournament=t).filter(friend=user)
            data = serializers.serialize("json", q, fields=("match_number", "home_score", "away_score", "home_win"))
            knockout_matches = [d["fields"] for d in json.loads(data)]

            q = TopScorer.objects.get(tournament=t, friend=user)
            output = {
                "group_matches": group_matches,
                "knockout_matches": knockout_matches,
                "top_scorer": q.name,
            }

        return JsonResponse(output)

    def post(self, request, uid=1):
        request_token = request.GET.get('token')
        if not request_token:
            return JsonResponse({}, status=401)

        try:
            user = get_user(request_token)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=403)

        return JsonResponse(PREDICTIONS)