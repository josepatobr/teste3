from django.core.validators import MinValueValidator
from django.db import models
from cadastro.models import Person
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify


class Produto(models.Model):
    nome = models.CharField(
        max_length=200,
        unique=True,
        error_messages={
            "unique": _("Produto com este nome já existe."),
        },
        help_text=_("Nome do produto"),
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        editable=False,
        help_text=_("Slug do produto - gerado automaticamente."),
    )
    descricao = models.TextField(
        blank=True,
        max_length=1000,
        help_text=_("Descrição detalhada do produto."),
    )
    imagem = models.ImageField(
        upload_to="produtos/",
        null=True,
        blank=True,
        help_text=_("Imagem do produto."),
    )
    valor = models.DecimalField(
        validators=[MinValueValidator(Decimal("0.01"))],
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Valor do produto em reais - mínimo R$ 0,01."),
    )
    is_active = models.BooleanField(default=True, help_text=_("Produto ativo."))
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("Data de criação.")
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("Data da última atualização.")
    )

    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")
        db_table = "produtos"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    @property
    def valor_formatado(self):
        from django.utils.formats import number_format

        return f"R$ {number_format(self.valor, 2)}"

    def __str__(self):
        return f"{self.nome} - {self.valor_formatado}"


class Vendedor(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name="vendedor",
        help_text=_("Pessoa associada ao vendedor."),
    )
    produtos = models.ManyToManyField(
        Produto,
        related_name="vendedores",
        blank=True,
        help_text=_("Produtos disponíveis para venda."),
    )
    is_active = models.BooleanField(default=True, help_text=_("Vendedor ativo."))
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("Data de criação.")
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("Data da última atualização.")
    )

    class Meta:
        verbose_name = _("Vendedor")
        verbose_name_plural = _("Vendedores")
        db_table = "vendedores"

    def __str__(self):
        return self.person.get_full_name()

    def get_active_produtos(self):
        return (
            self.produtos.select_related("vendedores")
            .filter(is_active=True, valor__gt=Decimal("0.00"))
            .order_by("nome")
        )
