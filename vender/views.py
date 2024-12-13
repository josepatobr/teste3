from django.shortcuts import render, redirect
from vender.models import Produto
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import *
import stripe
from django.views.decorators.csrf import csrf_exempt


def create_checkout_session(request, id):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        produto = Produto.objects.get(id=id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "BRL",
                        "unit_amount": int(produto.preco * 100),
                        "product_data": {"name": produto.nome},
                    },
                    "quantity": 1,
                }
            ],
            payment_method_types=["card", "boleto"],
            metadata={
                "id_produto": produto.id,
            },
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel")),
        )
        return redirect(checkout_session.url, code=303)
    else:
        return redirect("home")
def cancel(request):
    return render(request, "produto.html")



def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(request, "produto.html", {'produto': produto, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})




    
