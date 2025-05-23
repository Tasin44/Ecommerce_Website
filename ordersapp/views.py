
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from cartapp.views import get_or_create_cart
from .models import Order, OrderItem
from cartapp.models import Cart
from .forms import OrderCreateForm
from django.contrib import messages

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ordersapp/order_history.html', {'orders': orders})
'''
def order_create(request):
    # Initialize cart as None
    cart = None
    cart_items = []
    total_price = 0
    
    # Try to get the cart from session
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
            cart_items = cart.items.all()
            total_price = cart.get_total_price()
            
            # Check if cart is empty
            if not cart_items.exists():
                messages.warning(request, "Your cart is empty")
                return redirect("cartapp:cart_detail")
                
        except Cart.DoesNotExist:
            # If cart doesn't exist, clear the session
            del request.session['cart_id']
            messages.warning(request, "Your cart is no longer available")
            return redirect("cartapp:cart_detail")

    # Handle POST request
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Only proceed if we have a valid cart with items
            if not cart or not cart_items:
                messages.error(request, "Cannot create order with empty cart")
                return redirect("cartapp:cart_detail")
                
            # Create the order
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # Clear the cart
            cart.delete()
            del request.session['cart_id']
            
            messages.success(request, "Order placed successfully!")
            return redirect("ordersapp:order_confirmation", order.id)
    else:
        # Handle GET request
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}",
                'email': request.user.email,
            }
            form = OrderCreateForm(initial=initial_data)
        else:
            form = OrderCreateForm()
    
    return render(request, "ordersapp/order_create.html", {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
        "form": form
    })
'''
def order_create(request):
    cart = get_or_create_cart(request)  # Use the same function as cartapp
    
    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect("cartapp:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # Clear cart but preserve session
            cart.items.all().delete()
            messages.success(request, "Order placed successfully!")
            return redirect("ordersapp:order_confirmation", order.id)
    else:
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}",
                'email': request.user.email,
            }
            form = OrderCreateForm(initial=initial_data)
        else:
            form = OrderCreateForm()
    
    # Ensure session is saved
    request.session.modified = True
    return render(request, "ordersapp/order_create.html", {
        "cart": cart,
        "form": form
    })
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "ordersapp/order_confirmation.html", {
        "order": order,
        "order_items": order.items.all()
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "ordersapp/order_detail.html", {
        "order": order,
        "order_items": order.items.all()
    })
'''
from django.shortcuts import render,redirect, get_object_or_404
from cartapp.models import Cart
from .forms import OrderCreateForm
from .models import OrderItem,Order
# Create your views here.

def order_create(request):
    cart = None
    cart_id = request.session.get('cart_id')#retrieves the cart_id from the session.

    
    # If a cart_id exists, it tries to fetch the corresponding Cart object. If the cart is empty (cart.item.exists() is False), or doesn’t exist, it redirects to the cart detail page.
    
    if cart_id:
        cart = Cart.objects.get(id=cart_id)

        if not cart or not cart.items.exists():
            return redirect("cartapp:cart_detail")
        
    #if our users want to send the form after filling this
    if request.method=="POST":#request method POST means the user submitted the form.
        form = OrderCreateForm(request.POST)#takes the submitted data and checks if it’s valid using form.is_valid().
        
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
    # If the form is valid, it creates an Order object but does not save it to the database yet (commit=False). This allows you to add additional information before saving.

            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity
                )
    # Loops through all items in the cart and creates an OrderItem for each one, linking it to the newly created order. It saves the product, price, and quantity for each item.

            cart.delete()
            del request.session["cart_id"]     
    # Deletes the cart after processing the order and removes cart_id from the session.

            return redirect("ordersapp:order_confirmation",order.id)#Redirects to an order confirmation page, passing the newly created order's ID.
        
        else:#If the form is not valid, it re-renders the order creation page with any validation errors.
            form = OrderCreateForm()
        return render(request,"ordersapp/order_create.html",{
            "cart":cart, "form":form
        })
    
#Displays a confirmation page for the newly created order.
def order_confirmation(request,order_id):
    order = get_object_or_404(Order,id=order_id)#Fetches the Order using order_id. If it doesn’t exist, raises a 404 error.
    return render(request,"ordersapp/order_confirmation.html",{"order":order})
    #Passes the Order object to the order_confirmation.html template for rendering.
'''