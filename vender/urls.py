from django.urls import path
from . import views

urlpatterns = [
    path("produto/<str:slug>", views.produto, name="produto"),
    path('create-checkout-session/<int:id>', views.create_checkout_session, name="create_checkout_session"),

]
