from django.urls import path

from . import views

app_name = 'tournaments'
urlpatterns = [
    path('predictions', views.PredictionsView.as_view(), name='predictions'),
    path('euro2020', views.TournamentView.as_view(), name='euro2020'),
]