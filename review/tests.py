from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from review.models import ReviewEntry
from main.models import UserProfile
import json
import uuid

class ReviewTests(TestCase):
    def setUp(self):
        # Create test users with different roles
        self.client = Client()
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            role="user"
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='admin123'
        )
        UserProfile.objects.create(
            user=self.admin_user,
            role="admin"
        )
        
        # Create steakhouse owner user
        self.owner_user = User.objects.create_user(
            username='owneruser',
            password='owner123'
        )
        UserProfile.objects.create(
            user=self.owner_user,
            role="steakhouse owner"
        )
        
        # Create a sample review
        self.review = ReviewEntry.objects.create(
            user=self.user,
            menu="Test Steak",
            place="Test Place",
            rating=5,
            description="Test Description"
        )

    def test_model_methods(self):
        """Test ReviewEntry model methods"""
        self.assertTrue(self.review.is_menu_recommended)
        
        low_rated_review = ReviewEntry.objects.create(
            user=self.user,
            menu="Bad Steak",
            place="Bad Place",
            rating=3,
            description="Not good"
        )
        self.assertFalse(low_rated_review.is_menu_recommended)

    def test_show_review_view(self):
        """Test show_review view for different user roles"""
        # Test for regular user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('review:show_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')
        
        # Test for admin user
        self.client.login(username='adminuser', password='admin123')
        response = self.client.get(reverse('review:show_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_admin.html')
        
        # Test for owner user
        self.client.login(username='owneruser', password='owner123')
        response = self.client.get(reverse('review:show_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_owner.html')

    def test_add_review_entry_ajax(self):
        """Test adding review entry via AJAX"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'menu': 'New Steak',
            'place': 'New Place',
            'rating': '4',
            'description': 'New Description'
        }
        
        response = self.client.post(
            reverse('review:create-review-entry-ajax'),
            data=data
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            ReviewEntry.objects.filter(menu='New Steak').exists()
        )

    def test_edit_review(self):
        """Test editing a review"""
        self.client.login(username='testuser', password='testpass123')
        
        updated_data = {
            'menu': 'Updated Steak',
            'place': 'Updated Place',
            'rating': 4,
            'description': 'Updated Description'
        }
        
        response = self.client.post(
            reverse('review:edit_review', kwargs={'id': self.review.id}),
            data=updated_data
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        updated_review = ReviewEntry.objects.get(id=self.review.id)
        self.assertEqual(updated_review.menu, 'Updated Steak')

    def test_delete_review(self):
        """Test deleting a review"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('review:delete_review', kwargs={'id': self.review.id})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(
            ReviewEntry.objects.filter(id=self.review.id).exists()
        )

    def test_submit_reply(self):
        """Test submitting a reply to a review"""
        self.client.login(username='owneruser', password='owner123')
        
        data = {
            'review_id': str(self.review.id),
            'reply_text': 'Thank you for your review!'
        }
        
        response = self.client.post(
            reverse('review:submit_reply'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        updated_review = ReviewEntry.objects.get(id=self.review.id)
        self.assertEqual(updated_review.owner_reply, 'Thank you for your review!')

    def test_unauthorized_reply(self):
        """Test submitting a reply with unauthorized user"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'review_id': str(self.review.id),
            'reply_text': 'Unauthorized reply'
        }
        
        response = self.client.post(
            reverse('review:submit_reply'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 403)

    def test_json_endpoints(self):
        """Test JSON endpoints"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test show_json
        response = self.client.get(reverse('review:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Test show_json_by_id
        response = self.client.get(
            reverse('review:show_json_by_id', kwargs={'id': self.review.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_xml_endpoints(self):
        """Test XML endpoints"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test show_xml
        response = self.client.get(reverse('review:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        
        # Test show_xml_by_id
        response = self.client.get(
            reverse('review:show_xml_by_id', kwargs={'id': self.review.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')