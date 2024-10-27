from django.test import TestCase, Client
from django.urls import reverse
from booking.models import Booking
from explore.models import Menu
from django.contrib.auth.models import User
from django.utils import timezone

class BookingTestCase(TestCase):

    def setUp(self):
        # Membuat user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.owner = User.objects.create_user(username='owner', password='password')

        # Membuat menu items
        self.menu_item = Menu.objects.create(
            menu="Steak Special",
            restaurant_name="SteakHouse",
            price=150000,
            rating=4.5,
            city="Central Jakarta",
            image="http://example.com/steak.jpg"
        )

        # User login
        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_create_booking(self):
        # Membuat booking
        response = self.client.post(reverse('booking:booking_form', args=[self.menu_item.id]), {
            'booking_date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'number_of_people': 2
        })

        # Cek jika booking terbuat
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Booking.objects.filter(menu_items=self.menu_item, user=self.user).exists())

    def test_view_bookings(self):
        # Create booking
        booking = Booking.objects.create(
            menu_items=self.menu_item,
            user=self.user,
            booking_date=timezone.now(),
            number_of_people=2
        )

        # Cek user bisa mengecek atau tidak
        response = self.client.get(reverse('booking:lihat_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daftar Booking Anda')
        self.assertContains(response, 'Steak Special')

    def test_owner_view_booking(self):
        self.client.logout()
        self.client.login(username='owner', password='password')

        booking = Booking.objects.create(
            menu_items=self.menu_item,
            user=self.user,
            booking_date=timezone.now(),
            number_of_people=2
        )
        self.menu_item.claimed_by = self.owner
        self.menu_item.save()

        response = self.client.get(reverse('booking:pantau_booking_owner'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pantau Booking')
        self.assertContains(response, 'SteakHouse')

    def test_owner_delete_ownership(self):
        self.client.logout()
        self.client.login(username='owner', password='password')

        self.menu_item.claimed_by = self.owner
        self.menu_item.save()

        response = self.client.post(reverse('claim:delete_ownership', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 302) 
        self.menu_item.refresh_from_db()
        self.assertIsNone(self.menu_item.claimed_by)
