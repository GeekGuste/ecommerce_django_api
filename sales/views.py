from datetime import date
from django.shortcuts import render
from django.shortcuts import render
from importlib_metadata import metadata
from rest_framework import status
from rest_framework.response import Response
from sales.models import OrderProduct
from sales.models import Product
from sales.models import Order
 
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
        payment_method_types=['card'],
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
        return Response(status=status.HTTP_200_OK, data={'order_id': order.id})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Erreur de paiement, veuillez réessayer.'})

@csrf_exempt
@api_view(['POST'])
def save_order(request):
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

    return Response(status=status.HTTP_200_OK, data={'order': order.toJSON()})