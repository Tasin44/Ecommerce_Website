from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Users are inactive until email verification
    email_verification_token = models.CharField(max_length=64, blank=True)
    email_verification_token_created_at = models.DateTimeField(null=True, blank=True)
    
    # Add these required fields
    REQUIRED_FIELDS = ['email']  # For createsuperuser command
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def generate_email_verification_token(self):
        self.email_verification_token = get_random_string(64)
        self.email_verification_token_created_at = timezone.now()
        self.save()
        return self.email_verification_token