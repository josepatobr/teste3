from django.shortcuts import render, redirect
from vender.models import Produto
from django.shortcuts import get_object_or_404
from django.conf import settings
import stripe
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import *


def create_checkout_session(request, id):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        produto = Produto.objects.get(id=id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "BRL",
                        "unit_amount": int(produto.valor * 100),
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
        return redirect("produto", slug=produto.slug)


def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(request, "produto.html", {"produto": produto})


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    print(payload)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
            
        print('Aprovada')

    return HttpResponse(status=200)

