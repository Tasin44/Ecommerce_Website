

from django.conf import settings
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('PR', 'Processing'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('storeapp.Product', related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

'''
from django.db import models
from storeapp.models import Product
# Create your models here.

class Order(models.Model):
    full_name= models.CharField(max_length=250)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())#loop through the name of the orderitems and calculate the price

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items",on_delete=models.CASCADE)#foreign key relationship between OrderItem class and Order class 
    product = models.ForeignKey(Product,related_name="order_items",on_delete=models.CASCADE)
    #if an order is deleted the order item will also be deleted
    price = models.DecimalField(max_digits=10,decimal_places=2)#adding a price feild here good cause we want to calculate discounts 
    quantity = models.PositiveBigIntegerField(default=1)

    def get_cost(self):
        return self.price*self.quantity
    
# order: ForeignKey linking each OrderItem to an Order.
# (With related_name="items", you can access all OrderItems of an Order using order.items.all().)
# product: ForeignKey linking the item to a Product.
'''