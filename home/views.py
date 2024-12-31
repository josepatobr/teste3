from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from vender.models import Produto
from cadastro.models import Person


@login_required(login_url="cadastro")
def home(request):
    produtos = Produto.objects.all()
    return render(request, "home.html", {"produtos": produtos})


@login_required(login_url="cadastro")
def perfil(request: HttpRequest):
    user = request.user
    profile_image = user.profile_image.url if user.profile_image else None
    return render(request, "perfil.html", {"profile_image": profile_image})


def nome_perfil(request, username):
    person = get_object_or_404(Person, username=username) 
    return render(request, "perfil.html", {"person": person})


@login_required(login_url="cadastro")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("profile_image")
        request.user.profile_image = image
        request.user.save()
    return redirect("perfil")


    


