from django.urls import path
from . import views

urlpatterns = [
    path("predict/", views.DiabetesPredictionView.as_view(), name="predict-diabetes"),
]
