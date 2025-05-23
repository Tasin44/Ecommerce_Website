"""
URL configuration for ecomproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# Django usually checks the URL pattern in the order that they r 
# defined , so it check the cartapp.urls before the storeapp.urls
app_name = "cartapp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/',include('cartapp.urls')),
    path('',include('storeapp.urls')),
    path('ordersapp/',include('ordersapp.urls')),
    path('auth/',include('authapp.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
