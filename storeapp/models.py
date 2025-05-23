from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name=models.CharField(max_length=500)
    slug = models.SlugField(unique=True)#our urls will be make sense

    class Meta:# Adjusts the plural name to "categories" in the admin interface.
        verbose_name_plural = "categories"#saying django about the plural of category 

    def __str__(self):# Ensures categories are represented by their name in Django Admin and other interfaces.
        return self.name





class Product(models.Model):
    #every product will have to belong a category. lets create a one to many relationship between product and category where there are many categories and the product has to belong to them

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    #if the category table deleted, the products belongs to this category will also be delated
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField(blank=True)#we would like to allow blank to be true
    price = models.DecimalField(max_digits=10, decimal_places=2)#decimal_places means number after . like 3.45
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)#getting the time of adding a object or product
    updated = models.DateTimeField(auto_now=True)#the time of updation any product will also be added
    image = models.ImageField(upload_to='products', blank=True, null=True)
    average_rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.review_count = reviews.count()
        else:
            self.average_rating = 0
            self.review_count = 0
        self.save()
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):#Dynamically generates the product's URL based on its ID and slug.
        return reverse('storeapp:product_detail', kwargs={'id':self.id, 'slug':self.slug})#kwargs is a dictionary
    #reverse will help us to generate a urls pattern based on the arguments we provide,
    #reverse in models helps generate these URLs dynamically.


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')  # One review per user per product

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist"

'''
Slug:
if i click on tshirt1 , the urls look like:
http://127.0.0.1:8000/product/1/tshirt/
This what the slug doing,explain:

URL Example:

http://127.0.0.1:8000/product/1/tshirt/

    1: This is the unique identifier (id) of the product. It's the primary key from the database.
    
    tshirt: This is the slug, a URL-safe representation of the product name.

    
Purpose of the Slug

    Readability: The slug makes the URL easier to read and understand for users (e.g., tshirt instead of product?name=Tshirt).
    SEO Optimization: Including meaningful keywords (like product names) in the URL improves search engine rankings.
    Uniqueness: Slugs are unique per product or category, ensuring no conflicts in URLs.

    
How It’s Working

>>>>In Your Product Model:

slug = models.SlugField(max_length=250)
This defines the slug field, which is stored in the database for each product.



>>>>In the get_absolute_url Method:

def get_absolute_url(self):
    return reverse('storeapp:product_detail', kwargs={'id': self.id, 'slug': self.slug})

This method dynamically generates the URL for a product using its id and slug.



>>>>In Your Templates (list.html):

<a href="{% url 'storeapp:product_detail' product.id product.slug %}">
The URL tag uses the id and slug to create the link.


>>>Result:
When you click on a product (e.g., "Tshirt1"):

    Django looks for the product using the id and slug in the database.
    The view (product_detail) fetches the product and displays its details.
    The URL becomes http://127.0.0.1:8000/product/1/tshirt/, where:
        1 is the product's ID.
        tshirt is its slug.
'''


'''
Reason for Using ForeignKey:
1. Relationship Between Categories and Products:
    Each product must belong to one category
    Each category can have many products
    This is a one-to-many relationship, which is naturally modeled with a ForeignKey.

2.Database Design:
The ForeignKey creates a column in the (pgadmin) Product table that stores a reference (ID) of each product like Tshirt2 is category 1, shoe1 is category 4 etc
to the related Category table.

3.By using on_delete=models.CASCADE, deleting a category automatically deletes all its related products, 
'''