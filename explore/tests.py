from django.test import TestCase
import pytest
from django.urls import reverse
from django.test import TestCase
from .models import Menu
from .forms import MenuForm

class MenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu = Menu.objects.create(
            menu="Steak",
            category="Main Course",
            price=150000,
            restaurant_name="Steak House",
            city="Jakarta",
            specialized="Beef",
            rating=4.5,
            takeaway=True,
            delivery=True,
            outdoor=True,
            smoking_area=False,
            wifi=True,
            image="path/to/image.jpg"
        )

    def test_menu_content(self):
        self.assertEqual(self.menu.menu, "Steak")
        self.assertEqual(self.menu.price, 150000)

    def test_menu_str(self):
        self.assertEqual(str(self.menu), self.menu.menu)


class MenuFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'menu': 'Chicken Steak',
            'category': 'Main Course',
            'price': 120000,
            'restaurant_name': 'Chicken House',
            'city': 'Jakarta',
            'specialized': 'Chicken',
            'rating': 4.0,
            'takeaway': True,
            'delivery': True,
            'outdoor': False,
            'smoking_area': False,
            'wifi': True,
            'image': 'path/to/image.jpg',
        }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'menu': '',
            'category': 'Main Course',
            'price': 120000,
        }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())


class MenuViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu = Menu.objects.create(
            menu="Steak",
            category="Main Course",
            price=150000,
            restaurant_name="Steak House",
            city="Jakarta",
            specialized="Beef",
            rating=4.5,
        )

    def test_menu_list_view(self):
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertContains(response, "Steak")

    def test_menu_detail_view(self):
        response = self.client.get(reverse('menu_detail', args=[self.menu.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_detail.html')
        self.assertContains(response, "Steak")

    def test_edit_menu_view(self):
        response = self.client.get(reverse('edit_menu', args=[self.menu.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_menu.html')

    def test_create_menu_view(self):
        response = self.client.post(reverse('create_menu'), {
            'menu': 'Pasta',
            'category': 'Main Course',
            'price': 80000,
            'restaurant_name': 'Pasta House',
            'city': 'Jakarta',
            'specialized': 'Italian',
            'rating': 4.0,
            'takeaway': True,
            'delivery': False,
            'outdoor': True,
            'smoking_area': False,
            'wifi': True,
            'image': 'path/to/image.jpg',
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful creation
        self.assertEqual(Menu.objects.count(), 2)  # Ensure new menu is created


@pytest.mark.django_db
class MenuUrlTest(TestCase):
    def test_menu_urls(self):
        menu_list_url = reverse('menu_list')
        menu_detail_url = reverse('menu_detail', args=[1])  # assuming id 1 exists
        edit_menu_url = reverse('edit_menu', args=[1])  # assuming id 1 exists

        response = self.client.get(menu_list_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(menu_detail_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(edit_menu_url)
        self.assertEqual(response.status_code, 200)
