from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import *


# Create your views here.
def store(request):
    data = renderCart(request)
    order = data['order']

    products = Product.objects.all()
    context = {
        'products': products,
        'order': order,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = renderCart(request)
    order = data['order']
    orderitems = data['orderitems']

    context = {
        'order': order,
        'orderitems': orderitems,

    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = renderCart(request)
    order = data['order']
    orderitems = data['orderitems']

    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    product = Product.objects.get(id=product_id)

    orderitems, created = OrderItem.objects.get_or_create(product=product, order=order)

    if action == 'add':
        orderitems.quantity = orderitems.quantity + 1
    elif action == 'remove':
        orderitems.quantity = orderitems.quantity - 1
    orderitems.save()

    if orderitems.quantity <= 0:
        orderitems.delete()

    return JsonResponse("Item Added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    shippingInfo = data['shipping']
    userInfo = data['form']

    print(userInfo, "\n", shippingInfo)

    if request.user.is_authenticated:
        print("User is authenticated")
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(data, request)

    if userInfo['total'] == str(order.get_cart_total):
        print("Total corrected")
        order.transaction_id = transaction_id
        order.complete = True
    order.save()
    print("Shipping Address")

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=shippingInfo['address'],
            city=shippingInfo['city'],
            state=shippingInfo['state'],
            zipcode=shippingInfo['zipcode'],
            country=shippingInfo['country'],
        )

    return JsonResponse("Order Completed!", safe=False)
