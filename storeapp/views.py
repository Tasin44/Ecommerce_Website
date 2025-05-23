
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Review, Wishlist
from .forms import ReviewForm
from django.contrib import messages

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.all().order_by('-created_at')
    
    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(product=product, user=request.user)
        except Review.DoesNotExist:
            pass
    
    # Review form handling
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST, instance=user_review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            product.update_rating()
            messages.success(request, "Thank you for your review!")
            return redirect('storeapp:product_detail', id=id, slug=slug)
    else:
        review_form = ReviewForm(instance=user_review)
    
    # Check if product is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            products=product
        ).exists()
    
    return render(request, 'detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
        'related_products': Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
    })

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, f"{product.name} added to your wishlist")
    return redirect('storeapp:product_detail', id=product.id, slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    messages.success(request, f"{product.name} removed from your wishlist")
    return redirect('storeapp:product_detail', id=product.id, slug=product.slug)

@login_required
def wishlist_view(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    return render(request, 'storeapp/wishlist.html', {
        'wishlist': wishlist
    })



from django.shortcuts import render,get_object_or_404
from .models import Category,Product


#this is the view that will list all of our product
def product_list(request,category_slug=None):
#in order to filter by category ,we should pass in category_slug as a parameter that would help us filter 
    category=None
    products = Product.objects.filter(available=True)#all the products of our inventory 
    categories = Category.objects.all()#all the availabel category
    
    if category_slug:#if category slug is provided (explained below)
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)



    return render(request, 'list.html', {#Pass the data (categories, products, selected category) to the list.html(which will contain product list) template.
        'category':category,
        'products':products,
        'categories':categories,#passing all the available category 
    })



def product_detail(request, id, slug):#Displays detailed information about a single product.
    product = get_object_or_404(Product, id=id, slug=slug, available=True)#Retrieve a product based on its ID and slug.

    return render(request, 'detail.html', {'product':product})#Pass the product to the detail.html template for rendering.

'''
Filters products by category if a category_slug is provided.
How It Works:

No category_slug Provided (Default Case):
        If no category_slug is provided, the code:
            Retrieves all products that are marked as available=True.
            Does not filter by any specific category.
        Result: All products are displayed.

When category_slug is Provided:
        The category_slug is used to identify the category the user wants to view.
        
        The get_object_or_404(Category, slug=category_slug):
            Looks for the category with the matching slug.
            Raises a 404 error if no such category exists.
            
        If a valid category is found:
            The products are filtered using .filter(category=category).
        Result: Only the products in the specified category are displayed.
'''