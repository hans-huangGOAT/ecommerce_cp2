import json
from .models import *


def cookieData(request):
    orderitems = []
    order = {'get_total_items': 0, 'get_cart_total': 0, 'shipping': False}
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    for i in cart:
        print(i)
        product = Product.objects.get(id=i)

        orderitem = {
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "digital": product.digital,
                "imageURL": product.imageURL,
            },
            'quantity': cart[i]['quantity'],
            'get_total': cart[i]['quantity'] * product.price,
        }
        orderitems.append(orderitem)

        if not product.digital:
            order['shipping'] = True

        order['get_cart_total'] += orderitem['get_total']
        order['get_total_items'] += orderitem['quantity']
    return {
        'order': order,
        'orderitems': orderitems,
    }


def renderCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
    else:
        cookieD = cookieData(request)
        order = cookieD['order']
        orderitems = cookieD['orderitems']
    return {
        'order': order,
        'orderitems': orderitems,
    }


def guestOrder(data, request):
    name = data['form']['name']
    print(name)
    email = data['form']['email']
    print("User not authenticated")
    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    cookieD = cookieData(request)

    orderitemsInfo = cookieD['orderitems']

    for item in orderitemsInfo:
        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
        )
    return customer, order
