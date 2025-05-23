
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Cart, CartItem
from storeapp.models import Product
from django.contrib import messages

'''
def get_or_create_cart(request):
    """
    Helper function to get or create cart based on user session or authentication
    """
    if request.user.is_authenticated:
        # For authenticated users, try to get their cart or create one
        cart, created = Cart.objects.get_or_create(user=request.user)
        # If user has a session cart, merge it with their account cart
        session_cart_id = request.session.get('cart_id')
        if session_cart_id and session_cart_id != cart.id:
            try:
                session_cart = Cart.objects.get(id=session_cart_id)
                merge_carts(cart, session_cart)
                request.session['cart_id'] = cart.id
            except Cart.DoesNotExist:
                pass
    else:
        # For anonymous users, use session-based cart
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(session_key=request.session.session_key)
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create(session_key=request.session.session_key)
            request.session['cart_id'] = cart.id
    return cart
'''


def get_or_create_cart(request):
    if request.user.is_authenticated:
        # For authenticated users, get or create cart and ensure session is synced
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created or 'cart_id' not in request.session:
            request.session['cart_id'] = cart.id
    else:
        # For anonymous users
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(session_key=request.session.session_key)
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create(session_key=request.session.session_key)
            request.session['cart_id'] = cart.id
    
    # Ensure session is saved
    request.session.modified = True
    return cart
def merge_carts(destination_cart, source_cart):
    """
    Merge items from source cart to destination cart
    """
    for source_item in source_cart.items.all():
        try:
            dest_item = destination_cart.items.get(product=source_item.product)
            dest_item.quantity += source_item.quantity
            dest_item.save()
        except CartItem.DoesNotExist:
            source_item.cart = destination_cart
            source_item.save()
    source_cart.delete()

@require_POST
def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    
    cart_item.save()

    response_data = {
        "success": True,
        "message": f'Added {product.name} to cart',
        "cart_item_count": cart.items.count()
    }
    
    return JsonResponse(response_data)

# def cart_detail(request):
#     cart = get_or_create_cart(request)
    
#     if not cart or not cart.items.exists():
#         cart = None
        
#     return render(request, "cartapp/detail.html", {
#         "cart": cart,
#         "recommended_products": Product.objects.filter(available=True).order_by('?')[:4]  # Random recommended products
#     })
def cart_detail(request):
    cart = get_or_create_cart(request)
    
    if not cart or not cart.items.exists():
        cart = None
        
    context = {
        "cart": cart,
        "recommended_products": Product.objects.filter(available=True).order_by('?')[:4]
    }
    
    # Explicitly save the session to ensure cart_id persists
    request.session.modified = True
    
    return render(request, "cartapp/detail.html", context)

def cart_remove(request, product_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=product_id, cart=cart)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("cartapp:cart_detail")

@require_POST
def cart_update(request, product_id):
    """Update quantity of a specific cart item"""
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity', 1)
    
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({"success": False, "message": "Invalid quantity"}, status=400)
    
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()
    
    return JsonResponse({
        "success": True,
        "message": f"Updated {product.name} quantity",
        "new_quantity": cart_item.quantity,
        "new_total": cart.get_total_price()
    })

@require_POST
def cart_clear(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, "Cart cleared successfully")
    return redirect("cartapp:cart_detail")

def cart_item_count(request):
    """Get the total number of items in cart (for AJAX requests)"""
    cart = get_or_create_cart(request)
    count = cart.items.count() if cart else 0
    return JsonResponse({"count": count})

'''   
#Adding a Product to the Cart
@require_POST
def cart_add(request, product_id):# this view Accepts the product_id to identify which product to add.

    cart_id = request.session.get('cart_id')#Retrieves the cart ID from the session if it exists. This keeps the cart unique for each user.

    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)#If a cart exists in the session, fetch it from the database.
        except Cart.DoesNotExist:
            cart= Cart.objects.create()#If the cart ID is invalid (does not exist), create a new cart.

    else:#If there’s no cart in the session, create a new cart and store its ID in the session.
        cart = Cart.objects.create()
        request.session['cart_id']= cart.id
    

    product=get_object_or_404(Product,id=product_id)#Retrieves the product using its ID. If it doesn't exist, a 404 error is raised.

    cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)#Checks if the product is already in the cart. If it is, retrieves it; otherwise, creates a new CartItem.(explained below)

    #The variable created is True, if a new item is created means the product was not present there before

    if not created:#If the item already existed in the cart (created is False), it increases its quantity by 1.

        cart_item.quantity+=1
    
    cart_item.save()

    response_data = {#Prepares a JSON response indicating success and the product name.
        "success":True,
        "message": f'Added {product.name} to cart'
    }
    
    return JsonResponse(response_data)#Returns the JSON response back to the client.

#Displaying Cart Details
def cart_detail(request):
        
        cart_id = request.session.get('cart_id')#Retrieves cart_id from the session and initializes cart as None.
        cart=None

        if cart_id:#If cart_id exists, it fetches the corresponding Cart. If not found, a 404 error is raised.
            cart = get_object_or_404(Cart,id=cart_id)

        if not cart or not cart.items.exists():#If there’s no valid cart or if it has no items, it sets cart back to None.
            cart=None
        # return render(request,"cartapp/detail.html",{"cart":cart})
        return render(request, "cartapp/detail.html", {"cart": cart})#Renders the cart detail page, passing the cart object to the template.

#Removing an Item from the Cart
def cart_remove(request,product_id):
        cart_id = request.session.get('cart_id')
        cart = get_object_or_404(Cart, id=cart_id)
        item = get_object_or_404(CartItem, id=product_id, cart=cart)#Fetches the cart item using the product ID and cart reference. Raises a 404 error if not found.
        item.delete()
        
        return redirect("cartapp:cart_detail")#Redirects the user to the cart detail view after the item is removed.

'''
'''

(1)render: This function is used to generate an HTML response by combining a template with a context dictionary.

(2)get_object_or_404: This function retrieves an object from the database based on the given parameters. If the object doesn’t exist, it raises a 404 error.

(3)redirect: This function is used to redirect the user to a different URL.


(4)require_POST: This decorator ensures that the associated view function only accepts POST requests. It helps to prevent unwanted GET requests.


(5)JsonResponse: This class is used to return JSON data as an HTTP response. It's useful for sending data back to the client in a structured format.


(6)cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

What Does get_or_create Do?

# get_or_create is a shortcut in Django's ORM.
# It looks for an object in the database that matches the provided filter conditions (in this case, cart=cart and product=product).
# If such an object exists, it retrieves it.
# If it does not exist, it creates a new object with the specified values.


Why cart=cart and product=product?
cart=cart

    The first cart (before(left cart) =) is the field name in the CartItem model, which represents the cart this item belongs to (likely a ForeignKey to the Cart model).
    The second cart (after(right one) =) is the local variable in the code that holds the current cart instance.

product=product

    Similarly, the first product is the field name in the CartItem model that links the cart item to a specific product (likely a ForeignKey to the Product model).
    The second product is the local variable in the code that holds the product instance being added to the cart.

If created is False, it means the item was already in the cart, so we update its quantity.
If created is True, it means the item was not present before, so we add it to the cart using the CartItem model.
The CartItem model works by linking two instances: cart and product.
When we do cart=cart and product=product(right side one is new item), we are telling Django to associate the new item with the given cart and product instances.
'''