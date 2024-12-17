from django.urls import path
from . import views

urlpatterns = [
    path("cadastro_produto/", views.cadastro_produto, name="cadastro_produto")
]
