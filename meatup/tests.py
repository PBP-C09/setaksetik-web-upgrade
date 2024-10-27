from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Wishlist, MeatupRequest

class MeatupTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        self.wishlist_item = Wishlist.objects.create(
            owner=self.user1,
            item_name='Sample Item',
            description='A description for the sample item.'
        )

        self.meatup_request = MeatupRequest.objects.create(
            sender=self.user1,
            receiver=self.user2,
            wishlist=self.wishlist_item
        )

    def test_show_requests(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('meatup:show_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Item')

    def test_received_requests(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('meatup:received_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Item')

    def test_create_request(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('meatup:create_request', args=[self.wishlist_item.id]), {
            'receiver': self.user2.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MeatupRequest.objects.filter(sender=self.user1, receiver=self.user2).exists())

    def test_agree_request(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('meatup:agree_request', args=[self.meatup_request.id]))
        self.meatup_request.refresh_from_db()
        self.assertEqual(self.meatup_request.status, 'accepted')
        self.assertRedirects(response, reverse('main:request_list'))

    def test_decline_request(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('meatup:decline_request', args=[self.meatup_request.id]))
        self.meatup_request.refresh_from_db()
        self.assertEqual(self.meatup_request.status, 'declined')
        self.assertRedirects(response, reverse('main:request_list'))

    def test_delete_request(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('meatup:delete_request', args=[self.meatup_request.id]))
        self.assertFalse(MeatupRequest.objects.filter(id=self.meatup_request.id).exists())
        self.assertEqual(response.status_code, 200)

    def test_wishlist_list(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('meatup:wishlist_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.wishlist_item.item_name)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.client.get(reverse('meatup:show_requests'))
        self.assertRedirects(response, '/login?next=/meatup/')