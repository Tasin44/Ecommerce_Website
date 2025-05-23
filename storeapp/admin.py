from django.contrib import admin
from .models import Category,Product
# Register your models here.

# admin.site.register(Category)

#in admin.py , list_display fields like name, available , price they should be exactly same 
#as written in the models.py 

#using list_display, that we can customize our admin
#if we registe the model in this way like @admin.register(Category), then only prepopulated will work
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["name","slug"]# it means which fields will be displayed at the time of adding category
    prepopulated_fields = {'slug':('name',)}#Automatically generates the slug field based on the name.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #list_display contains that fields which will be display at the time of adding products
    list_display=["name","price","available","created","updated","category"]
    prepopulated_fields = {'slug':('name',)}
