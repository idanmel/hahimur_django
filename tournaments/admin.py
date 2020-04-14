from django.contrib import admin

from .models import Tournament, GroupMatch, KnockOutMatch, GroupMatchPrediction, KnockOutMatchPrediction, Token

admin.site.register([
    Tournament,
    GroupMatch,
    KnockOutMatch,
    GroupMatchPrediction,
    KnockOutMatchPrediction,
    Token
])
