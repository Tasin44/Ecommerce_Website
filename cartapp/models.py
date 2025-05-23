from django.conf import settings
from django.db import models
from storeapp.models import Product 
#if we want to import one app model to another app model(storeapp model to cartapp)

# class Cart(models.Model):
#     created_at = models.DateField(auto_now_add=True)#so that we can track when our cart was created

#     def get_total_price(self):#This method help us to calculate total price of the items of the cart
#         return sum(item.get_total_price() for item in self.items.all())

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart,related_name="items",on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,related_name="cart_items",on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
#     def get_total_price(self):
#         return self.product.price * self.quantity
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('storeapp.Product', related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.product.price * self.quantity

#models.foreignkey using here cause we want to stublish here many to one relationship between models like in cart:relationship between CartItem model with Cart model, in product: relationship between CartItem model with Product model of storeapp

#models.ForeignKey(Cart,  --->Cart specifying the model we want to be relationship to be with(Cart model is situated CartItem above)

#on_delete=models.CASCADE) ---> it means once a cart is deleted ,the cart item will be also delated 






