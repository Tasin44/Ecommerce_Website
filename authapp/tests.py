from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        # Create superuser with proper attributes
        self.admin = User.objects.create_superuser(
            username='admin44',
            email='admin44@example.com',
            password='testpass123'
        )
        self.admin.is_active = True
        self.admin.save()

    def test_admin_login(self):
        """Test admin can log in to admin site"""
        # Test basic authentication
        logged_in = self.client.login(username='admin44', password='testpass123')
        self.assertTrue(logged_in)
        
        # Verify session
        session = self.client.session
        self.assertIn('_auth_user_id', session)
        self.assertEqual(str(session['_auth_user_id']), str(self.admin.pk))

    def test_admin_access(self):
        """Test admin can access admin dashboard"""
        self.client.login(username='admin44', password='testpass123')
        response = self.client.get(reverse('admin:index'))
        
        # Should return 200 for authenticated admin
        self.assertEqual(response.status_code, 200)
        
        # Verify user in context is our admin
        self.assertEqual(response.context['user'].username, 'admin44')