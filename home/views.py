from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from vender.models import Vendedores


@login_required(login_url="cadastro")
def home(request):
    return render(request, "home.html")


@login_required(login_url="cadastro")
def perfil(request: HttpRequest):
    user = request.user
    profile_image = user.profile_image.url if user.profile_image else None
    return render(request, "perfil.html", {"profile_image": profile_image})


@login_required(login_url="cadastro")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("profile_image")
        request.user.profile_image = image
        request.user.save()
    return redirect("perfil")


def mostrar_venda(request):
    produtos = Vendedores.objects.all()
    return render(request, "home.html", {"produtos": produtos})

