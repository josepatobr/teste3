from django.shortcuts import render
from vender.models import Produto
from django.shortcuts import get_object_or_404


def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(request, "produto.html", {"produto": produto})
