from django.urls import path
from . import views

app_name = "cartapp"

urlpatterns = [
    # Add item to cart (POST only)
    path('add/<int:product_id>/', views.cart_add, name="cart_add"),
    
    # View cart contents
    path("", views.cart_detail, name="cart_detail"),
    
    # Remove item from cart
    path("remove/<int:product_id>/", views.cart_remove, name="remove_item"),
    
    # Additional useful endpoints you might want to add:
    
    # Update item quantity (POST: quantity)
    path("update/<int:product_id>/", views.cart_update, name="update_item"),
    
    # Clear entire cart
    path("clear/", views.cart_clear, name="clear_cart"),
    
    # Get cart item count (AJAX)
    path("count/", views.cart_item_count, name="cart_item_count"),
]

'''
(1)path('add/<int:product_id>/', cart_add, name="cart_add"),

The URL pattern add/<int:product_id>/ specifies that this route will handle requests to /add/ followed by an integer representing the product ID (e.g., 127.0.0.1:8000/add/5/).

URL: /add/<product_id>/
Purpose: Calls the cart_add view when a user adds a product to the cart.
Dynamic Parameter: <int:product_id> captures the product's ID and passes it to the cart_add view.
Name: cart_add — used for referencing this URL.


(2)path("", cart_detail, name="cart_detail"),

URL Pattern: The empty string "" means this route will handle requests to the root URL of this app (e.g., /cart/).
View Function: It calls the cart_detail view function when accessed.
Name: cart_detail — used for referencing this URL.

(3)path("remove/<int:product_id>/", cart_remove, name="remove_item")

URL Pattern: The pattern remove/<int:product_id>/ specifies that this route will handle requests to /remove/ followed by an integer (the product ID) (e.g., /remove/5/).

View Function: It calls the cart_remove view function when accessed.

Name: remove_item — used for referencing this URL.
'''