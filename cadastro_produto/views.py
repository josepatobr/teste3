from django.shortcuts import render, redirect
from vender.models import Produto
from django.contrib import messages
from cadastro.email import send_email
from django.contrib.auth.decorators import login_required


@login_required(login_url="cadastro")
def cadastro_produto(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        imagem = request.FILES.get("imagem")

        if not nome or not valor or not descricao:
            messages.error(request, "Por favor, preencha todos os campos.")
            return redirect("cadastro_produto")

        try:
            produto = Produto.objects.create(
                nome=nome, valor=valor, descricao=descricao, imagem=imagem
            )
            email_subject = f'Você esta vendendo o produto "{produto.nome}"!'
            email_template = "email/produto.html"
            send_email(request.user, email_subject, email_template, produto=produto)

            messages.success(request, "Produto adicionado com sucesso!")
            return redirect("cadastro_produto")
        except Exception as e:
            messages.error(request, f"Erro ao criar o produto: {str(e)}")
            return redirect("cadastro_produto")
    produtos = Produto.objects.all()
    return render(request, "cadastro_produto.html", {"produtos": produtos})
