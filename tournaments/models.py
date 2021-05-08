from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint


class Tournament(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Group(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.tournament} - {self.name}"


class Team(models.Model):
    """A team"""
    name = models.CharField(max_length=200)
    flag = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

DEFAULT_TEAM = Team(name="Euro2020 Eliminations Placeholder",
                    flag="https://upload.wikimedia.org/wikipedia/en/9/96/UEFA_Euro_2020_Logo.svg")


class MatchInfo(models.Model):
    match_id = models.IntegerField(null=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateTimeField()
    ordering = ['date']

    def __str__(self):
        return f"{self.group}: {self.home_team} - {self.away_team}"

    class Meta:
        verbose_name_plural = "Matches Info"


class MatchScore(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE)
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    home_win = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.match_info}, {self.home_score} - {self.away_score}"


class MatchPrediction(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="mp_home_team", default=1)
    home_score = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="mp_away_team", default=1)
    away_score = models.IntegerField()
    home_win = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f"{self.friend}, {self.match_info.group}, {self.home_team} {self.home_score} -  {self.away_team} {self.away_score}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['match_info', 'friend'], name='unique_match_friend_prediction')
        ]


class Token(models.Model):
    token = models.CharField(max_length=200)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.friend}: {self.token}"


class TopScorer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Tournament: {self.tournament}, friend: {self.friend}, Top Scorer: {self.name}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['tournament', 'friend'], name='unique_top_scorer')
        ]
