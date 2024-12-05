from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from cadastro.models import Person


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def perfil(request: HttpRequest):
    user = Person.objects.get(id=request.user.id)
    profile_image = user.profile_image.url if user.profile_image else None
    return render(request, "perfil.html", {"profile_image": profile_image})


@login_required
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("profile_image")
        request.user.profile_image = image
        request.user.save()
    return redirect("perfil")
