from django.shortcuts import render, redirect
from vender.models import Produto
from django.contrib import messages

def cadastro_produto(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        imagem = request.FILES.get("imagem")

     
        if not nome or not valor or not descricao:
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, "cadastro_produto.html")

        try:
            produto = Produto.objects.create(nome = nome, valor = valor, descricao = descricao, imagem = imagem)
            messages.success(request, "Produto adicionado com sucesso!")
            return redirect("cadastro_produto")
        
        except Exception as e:
            messages.error(request, f"Erro ao criar o produto: {str(e)}")

    produtos = Produto.objects.all()
    return render(request, "cadastro_produto.html", {"produtos": produtos})


