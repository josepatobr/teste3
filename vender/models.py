from django.db import models
from django.core.validators import MinValueValidator


class Vendedores(models.Model):
    nome_vendedor = models.CharField(max_length=200, blank=False, editable=True)
    Produto = models.CharField(max_length=50, blank=False, editable=True)
    imagem_produto = models.ImageField(blank=False, editable=True, upload_to='media/vendedores/')
    valor = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0.01)], 
    default=0.00)

    def __str__(self):
        return self.nome_vendedor
