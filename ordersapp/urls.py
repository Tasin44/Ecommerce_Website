
from django.urls import path
from . import views

app_name = "ordersapp"

urlpatterns = [
    path('create/', views.order_create, name="order_create"),
    path('confirmation/<int:order_id>/', views.order_confirmation, name="order_confirmation"),
    path('history/', views.order_history, name="order_history"),
    path('detail/<int:order_id>/', views.order_detail, name="order_detail"),
]