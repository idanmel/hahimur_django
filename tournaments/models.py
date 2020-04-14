from django.conf import settings
from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GroupMatch(models.Model):
    """Only save matches that were already played!"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    match_number = models.IntegerField()

    def __str__(self):
        return f"{self.match_number}. {self.home_score} - {self.away_score}"

    class Meta:
        verbose_name_plural = "Group matches"


class KnockOutMatch(models.Model):
    """Only save matches that were already played!"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    match_number = models.IntegerField()
    home_win = models.BooleanField()

    def __str__(self):
        return f"{self.match_number}. {self.home_score} - {self.away_score} home_win: {self.home_win}"

    class Meta:
        verbose_name_plural = "Knock Out matches"


class GroupMatchPrediction(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match_number = models.IntegerField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return f"{self.friend}, {self.tournament} {self.match_number}. " \
               f"{self.home_score} - {self.away_score}"


class KnockOutMatchPrediction(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match_number = models.IntegerField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    home_win = models.BooleanField()

    def __str__(self):
        return f"{self.friend}, {self.tournament} {self.match_number}. " \
               f"{self.home_score} - {self.away_score} home_win: {self.home_win}"


class Token(models.Model):
    token = models.CharField(max_length=200)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.friend}: {self.token}"
