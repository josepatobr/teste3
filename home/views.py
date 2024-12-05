from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

@login_required
def perfil(request):
    return render(request, "perfil.html")

@login_required
def salvar_imagem(request):
    if request.method == "POST" and request.FILES.get("profile_image"):
        image = request.FILES["profile_image"]
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        return render(request, "perfil.html", {"image_url": uploaded_file_url})
    return redirect("perfil")
