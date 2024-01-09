# Third-party imports
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import Mock

# Local imports
from .models import BeeYard, Harvest, Hive


##### Models Tests #####


class HarvestTest(TestCase):
    def create_quantity(self, quantity=11.3):
        return Harvest.objects.create(quantity=quantity)

    def test_quantity_creation(self):
        quantity_test_obj = self.create_quantity()
        self.assertTrue(isinstance(quantity_test_obj, Harvest))
        expected_response = "11.3 kilograms"
        self.assertEqual(expected_response, quantity_test_obj.__str__())


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
        # A 401 error is expected without authentication
        self.assertEqual(resp.status_code, 401)

    def test_beeyard_access_authenticated(self):
        self.user = User.objects.create_user(username="TestUser1", password="TestPW123")
        self.client = Client()
        request = Mock()
        request.user = self.user
        self.client.force_login(self.user)
        test_yard = BeeYard.objects.create(name="TestYard1", beekeeper=self.user)
        test_hive = Hive.objects.create(
            status="pending",
            species="Buckfast bee",
            beeyard=test_yard,
            queen_year=2022,
            name="A",
        )
        url = reverse("show_beeyards")
        resp = self.client.get(url)

        # Log out
        self.client.logout()
        # A 200 code is expected for an authenticated user
        self.assertEqual(resp.status_code, 200)
        # The returned page should contain the name of the user's beeyard
        self.assertContains(resp, "TestYard1")
