from django.shortcuts import render, redirect
from vender.models import Produto
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import *
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, id):
    if request.method == "POST":
        produto = Produto.objects.get(id = id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
            {
                'price_data': {
                'currency': 'BRL',
                'unit_amount': int(produto.valor),
                    'product_data': {
                        'name': produto.nome
                    }

                },
                'quantity': 1,
            },
        ],
            payment_method_types=[
                'card',
                'boleto',
            ],
            metadata={
                'id_produto': produto.id,
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/sucesso',
            cancel_url=YOUR_DOMAIN + '/erro',
            )
        return redirect(create_checkout_session.url)
    else:
        return redirect("home")

def cancel(request):
    return render(request, "produto.html")


@csrf_exempt
def stripe_webnook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = settings.STRIPE_WEBNOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    print(payload)

    return HttpResponse(status=200)

def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(request, "produto.html", {'produto': produto, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})




    
