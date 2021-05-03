from django.contrib import admin

from .models import Tournament, Group, Team, MatchInfo, MatchScore, MatchPrediction, Token, TopScorer

admin.site.register([
    Tournament,
    Group,
    Team,
    MatchInfo,
    MatchScore,
    MatchPrediction,
    Token,
    TopScorer
])
