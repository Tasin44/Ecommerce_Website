from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from .forms import SignUpForm, LoginForm
from .models import CustomUser
from django.conf import settings
import datetime
from django.core.mail import EmailMessage
import socket

def send_verification_email(request, user):
    try:
        token = user.generate_email_verification_token()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        
        # Create email message
        email = EmailMessage(
            mail_subject,
            render_to_string('authapp/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            }),
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email.content_subtype = "html"  # Set content type to HTML
        
        # Try to send the email
        email.send(fail_silently=False)
        return True
    except socket.gaierror:
        # Handle DNS resolution errors
        print("Failed to resolve SMTP server address. Check your EMAIL_HOST setting.")
        return False
    except Exception as e:
        # Handle other email sending errors
        print(f"Failed to send verification email: {str(e)}")
        return False
    
# def send_verification_email(request, user):
#     token = user.generate_email_verification_token()
#     current_site = get_current_site(request)
#     mail_subject = 'Activate your account'
#     message = render_to_string('authapp/verification_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': token,
#     })
#     send_mail(
#         mail_subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         html_message=message,
#         fail_silently=False,
#     )
# authapp/views.py
import logging
logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            try:
                # Send verification email
                email_sent = send_verification_email(request, user)
                
                if email_sent:
                    messages.success(request, 'Account created! Check your email to activate.')
                    # Log successful email sending
                    logger.info(f"Verification email sent to {user.email}")
                else:
                    messages.warning(request, 'Account created but email not sent. Contact support.')
                    # Log email sending failure
                    logger.warning(f"Failed to send verification email to {user.email}")
                
                return redirect('authapp:login')
            
            except Exception as e:
                # Log the actual error
                logger.error(f"Error during signup: {str(e)}", exc_info=True)
                messages.error(request, 'Account creation failed. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'authapp/signup.html', {'form': form})
# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # User inactive until email verification
#             user.save()
            
#             # Send verification email
#             email_sent = send_verification_email(request, user)
            
#             if email_sent:
#                 messages.success(request, 'Account created successfully! Please check your email to activate your account.')
#             else:
#                 messages.warning(request, 'Account created, but we couldn\'t send the verification email. Please contact support.')
            
#             return redirect('authapp:login')
#     else:
#         form = SignUpForm()
#     return render(request, 'authapp/signup.html', {'form': form})
# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # User inactive until email verification
#             user.save()
            
#             # Send verification email
#             send_verification_email(request, user)
            
#             messages.success(request, 'Account created successfully! Please check your email to activate your account.')
#             return redirect('authapp:login')
#     else:
#         form = SignUpForm()
#     return render(request, 'authapp/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and user.email_verification_token == token:
        # Check if token is not expired (e.g., 24 hours)
        token_age = timezone.now() - user.email_verification_token_created_at
        if token_age < datetime.timedelta(days=1):
            user.is_active = True
            user.email_verification_token = ''
            user.save()
            messages.success(request, 'Your account has been activated successfully! You can now login.')
            return redirect('authapp:login')
        else:
            messages.error(request, 'The activation link has expired. Please request a new one.')
            return redirect('authapp:resend_activation')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('authapp:signup')

def resend_activation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email, is_active=False)
            send_verification_email(request, user)
            messages.success(request, 'A new activation email has been sent. Please check your inbox.')
            return redirect('authapp:login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No inactive account found with this email address.')
    
    return render(request, 'authapp/resend_activation.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('storeapp:product_list')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('storeapp:product_list')
                else:
                    messages.error(request, 'Your account is not active. Please check your email for the activation link.')
                    return redirect('authapp:resend_activation')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'authapp/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('storeapp:product_list')