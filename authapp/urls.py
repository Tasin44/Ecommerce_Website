from django.urls import path
from . import views

app_name = "authapp"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),
]