from django.urls import path
from . import views

urlpatterns = [
    path("produto/<str:slug>", views.produto, name="produto"),
]
