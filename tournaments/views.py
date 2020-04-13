from django.http import JsonResponse


def get_user(request_token):
    if request_token == "good_token":
        return "User"
    return None


def predictions(request, uid=1):
    request_token = request.GET.get('token')
    if not request_token:
        return JsonResponse({}, status=401)

    user = get_user(request_token)
    if not user:
        return JsonResponse({}, status=403)

    return JsonResponse({})
