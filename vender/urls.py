from django.urls import path
from . import views

urlpatterns = [
    path("produto/<str:slug>", views.produto, name="produto"),
    path("create-checkout-session/<int:id>", views.create_checkout_session,name="create_checkout_session"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path('stripe_webhook', views.stripe_webhook, name="stripe_webhook")
]
