from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from explore.models import Menu
from spinthewheel.models import SpinHistory
from django.utils import timezone
import json

User = get_user_model()

class SpinTheWheelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.menu_item = Menu.objects.create(menu="Steakhouse Special", category="Beef", restaurant_name="Steakhouse A")
        self.spin_history = SpinHistory.objects.create(user=self.user, winner=self.menu_item.menu, spin_time=timezone.now())

    def test_spin_view_access(self):
        """Check spin view access for a logged-in user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("spinthewheel:spin_view"))
        self.assertEqual(response.status_code, 200)

    def test_history_json_response(self):
        """Ensure history_json returns correct JSON data for spin history."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("spinthewheel:history_json"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]["fields"]["winner"], "Steakhouse Special")

    def test_option_json_filter(self):
        """Check option_json returns filtered menu items by category."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("spinthewheel:option_json", args=["Beef"]))
        data = json.loads(response.content)
        self.assertEqual(data[0]["fields"]["category"], "Beef")

    def test_add_spin_history(self):
        """Verify spin history is created on valid post request."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("spinthewheel:add_spin_history"), {"winner": "Steakhouse Special"})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(SpinHistory.objects.filter(user=self.user, winner="Steakhouse Special").exists())

    def test_delete_spin_history(self):
        """Test that a spin history entry can be deleted."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("spinthewheel:delete_spin_history", args=[self.spin_history.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after delete
        self.assertFalse(SpinHistory.objects.filter(id=self.spin_history.id).exists())
