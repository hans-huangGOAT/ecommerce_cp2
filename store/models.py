from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        try:
            return self.name
        except:
            return "error Name"


class Product(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    image = models.ImageField(default='cart_image_placeholder.png', null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    complete = models.BooleanField(default=False, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if not orderitem.product.digital:
                shipping = True
        return shipping

    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.quantity for orderitem in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.get_total for orderitem in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.address
