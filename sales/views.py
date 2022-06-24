from datetime import date
import email
from email import message
from django.shortcuts import render
from django.shortcuts import render
from importlib_metadata import metadata
from rest_framework import status
from rest_framework.response import Response
from sales.models import Contact
from sales.models import OrderProduct
from sales.models import Product
from sales.models import Order
from django.core.mail import send_mail, mail_admins
 
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

@csrf_exempt
@api_view(['POST'])
def create_payment(request):
    data = request.data
    email = data['email']
    items = data['items']
    total = float(data['delivery_charges'])
    
    for item in items:
        total += float(item['quantity']) * float(item['price'])
    #create order
    payment_intent = stripe.PaymentIntent.create(
        amount=int(total * 100), 
        currency='eur', 
        payment_method_types=['card', 'klarna'],
        receipt_email=email,
    )
    return Response(status=status.HTTP_200_OK, data={'payment_intent': payment_intent})

@csrf_exempt
@api_view(['POST'])
def confirm_payment(request):
    data = request.data
    intent_id = data['intent_id']
    rep = stripe.PaymentIntent.confirm(
        intent_id,
        payment_method='pm_card_visa',
    )
    if(rep):
        data = request.data
        email = data['email']
        items = data['items']
        total = float(data['delivery_charges'])
        order = Order(
            email = email,
            last_name = data['last_name'],
            first_name = data['first_name'],
            phone_number = data['phone_number'],
            address = data['address'],
            postal_code = data['postal_code'],
            country = data['country'],
            town = data['town'],
            delivery_charges = float(data['delivery_charges']),
            total = total,
            payment_date = date.today(),
            mode_paiement = "carte bancaire",
            user = request.user
        )
        order.is_paid = True
        order.save()
        for item in items:
            product = Product.objects.get(pk=item['id'])
            orderProduct = OrderProduct(
                product=product, 
                label=item['label'], 
                price = float(item['price']), 
                quantity=float(item['quantity']), 
                order = order,
                image_url = item['image']
            )
            orderProduct.save()
            #reduce quantity
            product.qte_stock = float(product.qte_stock) - float(item['quantity'])
            product.save()
            total += float(item['quantity']) * float(item['price'])
        order.total = total
        order.save()
        htmlMessage = ('Bonjour ' + order.first_name + '<br/>' +
            'Votre commande de ' + str(total) + '€ sur hocheacreation.fr a été validée. Votre/vos produit(s) sera livré dans les prochains jours.' + '<br/>' +
            '<br/>' +
            'L\'équipe Hochea');
        #Send email to hochea and client
        send_mail(
            subject='Votre commande a été validée',
            message=htmlMessage,
            html_message=htmlMessage,
            from_email='no-reply@hochea.tincom.biz',
            recipient_list=[email],
            fail_silently=True,
        )

        htmlMessage = 'Bonjour, <br/>' + 'La commande #'+str(order.id) + 'vient d\'être effectuée sur le site hocheacreation.fr<br/>'
        mail_admins(
            subject='Une nouvelle commande a été effectuée',
            html_message=htmlMessage,
            message=htmlMessage,
            fail_silently=True,
        )
        return Response(status=status.HTTP_200_OK, data={'order_id': order.id})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Erreur de paiement, veuillez réessayer.'})

@csrf_exempt
@api_view(['POST'])
def save_paypal_order(request):
    data = request.data
    email = data['email']
    items = data['items']
    total = float(data['delivery_charges'])
    order = Order(
        email = email,
        last_name = data['last_name'],
        first_name = data['first_name'],
        phone_number = data['phone_number'],
        address = data['address'],
        postal_code = data['postal_code'],
        country = data['country'],
        town = data['town'],
        delivery_charges = float(data['delivery_charges']),
        total = total,
        mode_paiement = "Paypal",
        is_paid = True,
        user = request.user
    )
    order.save()
    for item in items:
        product = Product.objects.get(pk=item['id'])
        orderProduct = OrderProduct(
            product=product, 
            label=item['label'], 
            price = float(item['price']), 
            quantity=float(item['quantity']), 
            order = order,
            image_url = item['image']
        )
        orderProduct.save()
        #reduce quantity
        product.qte_stock = float(product.qte_stock) - float(item['quantity'])
        product.save()
        total += float(item['quantity']) * float(item['price'])
    order.total = total
    order.save()
    #Send email to hochea and client
    
    return Response(status=status.HTTP_200_OK, data={'order_id': order.id})

@csrf_exempt
@api_view(['POST'])
def contact(request):
    data = request.data
    contact = Contact(
        email = data['email'],
        name = data['name'],
        message = data['message']
    )
    contact.save()

    htmlMessage = ('Bonjour, <br/>' + 
    'Le client ' + 
    contact.name + "("+ contact.email +")" + 
    ' a envoyé le message ci dessous depuis le formulaire de contact<br/><br/><br/>' +
    contact.message)

    mail_admins(
        subject='Message reçu depuis le formulaire de contact hochea',
        html_message=htmlMessage,
        message=htmlMessage,
        fail_silently=True,
    )

    return Response(status=status.HTTP_200_OK, data={'contact_id': contact.id})