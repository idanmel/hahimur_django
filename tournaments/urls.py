from django.urls import path

from . import views

app_name = 'tournaments'
urlpatterns = [
    path('predictions', views.PredictionsView.as_view(), name='predictions'),
]