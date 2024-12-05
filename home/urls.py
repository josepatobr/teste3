from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("perfil/", views.perfil, name="perfil"), 
    path("salvar_imagem/", views.salvar_imagem, name="salvar_imagem"),  
]
