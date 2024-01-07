# Third-party imports
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import Mock

# Local imports
from .models import BeeYard, Quantity


##### Models Tests #####


class QuantityTest(TestCase):
    def create_quantity(self, quantity=11.3, units="Kilograms"):
        return Quantity.objects.create(quantity=quantity, units=units)

    def test_quantity_creation(self):
        quantity_test_obj = self.create_quantity()
        self.assertTrue(isinstance(quantity_test_obj, Quantity))
        self.assertEqual("11.3 Kilograms", quantity_test_obj.__str__())


class BeeYardAccessTest(TestCase):
    def create_keeper(
        self,
        username="TestUser",
        password="Testing123",
        first_name="Test",
        last_name="User",
        email="test@test.com",
    ):
        return User.objects.create(
            username=username,
            password=password,
            last_name=last_name,
            first_name=first_name,
            email=email,
        )

    def create_beeyard(self, beekeeper, name="TestYard"):
        return BeeYard.objects.create(beekeeper=beekeeper, name=name)

    def test_beeyard_creation(self):
        test_user = self.create_keeper()
        test_yard = self.create_beeyard(beekeeper=test_user)
        self.assertTrue(isinstance(test_yard, BeeYard))

    def test_beeyard_access_notauthenticated(self):
        url = reverse("show_beeyards")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    def test_beeyard_access_authenticated(self):
        self.user = User.objects.create_user(username="TestUser1", password="TestPW123")
        self.client = Client()
        request = Mock()
        request.user = self.user
        self.client.force_login(self.user)
        test_yard = BeeYard.objects.create(name="TestYard1", beekeeper=self.user)

        url = reverse("show_beeyards")
        resp = self.client.get(url)

        # Log out
        self.client.logout()
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "TestYard1")
