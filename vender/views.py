from django.shortcuts import render
from .models import Vendedores

def mostrar_vendas(request):
    produtos = Vendedores.objects.all()
    return render(request, 'mostrar_vendas.html', {'produtos': produtos})
