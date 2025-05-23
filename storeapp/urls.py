from django.urls import path
from . import views

app_name = "storeapp"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name="product_detail"),
    path('wishlist/', views.wishlist_view, name="wishlist"),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name="remove_from_wishlist"),
]