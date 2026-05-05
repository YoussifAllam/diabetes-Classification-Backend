from django.urls import path

from . import views

urlpatterns = [
    path("predict/", views.DiabeticFootUlcerPredictView.as_view(), name="dfu-predict"),
]
