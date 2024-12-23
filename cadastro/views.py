from django.shortcuts import redirect, render
from .models import Person
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout
from .email import send_email


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("password")

        if not username or not email or not senha:
            messages.error(request, "por favor, preencha todos os campos")
            return redirect("cadastro")

        if len(username) <= 3 or len(username) >= 200:
            messages.error(request, "máximo de letras é 200 e o mínimo é de 3")
            return redirect("cadastro")

        if len(senha) < 4 or len(senha) > 20:
            messages.error(
                request,
                "senha deve ter no mínimo 4 caracteres e no máximo 20 caracteres",
            )
            return redirect("cadastro")

        if " " in senha:
            messages.error(request, "a senha não pode ter espaço")
            return redirect("cadastro")

        if Person.objects.filter(email=email, username=username).exists():
            messages.error(request, "Usuário ja existe")
            return redirect("cadastro")

        try:
            user = Person.objects.create_user(
                username=username, email=email, password=senha
            )

            email_subject = f"Welcome, {user.get_short_name()}!"
            email_template = "emails/welcome.html"
            send_email(user, email_subject, email_template)

            django_login(request, user)
            messages.success(request, "Usuário criado com sucesso")
            return redirect("cadastro")
        except Exception as e:
            print(e)
            messages.error(request, "erro ao criar a conta")
            return redirect("cadastro")
    return render(request, "cadastro.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method != "POST":
        return redirect("cadastro")

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        messages.error(request, "por favor, preencha todos os campos")
        return redirect("cadastro")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return redirect("home")

    messages.error(request, "Usuário ou senha inválidos")
    return redirect("cadastro")


def sair(request):
    logout(request)
    return redirect("cadastro")
