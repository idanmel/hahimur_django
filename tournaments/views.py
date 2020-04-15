from django.http import JsonResponse
from .models import Token
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
    def get(self, request):
        request_token = request.GET.get('token')
        if not request_token:
            return JsonResponse({}, status=401)

        try:
            user = get_user(request_token)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=403)

        return JsonResponse(PREDICTIONS)

    def post(self, request):
        request_token = request.GET.get('token')
        if not request_token:
            return JsonResponse({}, status=401)

        try:
            user = get_user(request_token)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=403)

        return JsonResponse(PREDICTIONS)