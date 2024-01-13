# Third-party imports
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import Mock

# Local imports
from .models import BeeYard, Contamination, Harvest, Hive


##### Models Tests #####
class HarvestTest(TestCase):
    """A class for testing the Harvest model and its related functions."""

    def create_harvest(self, quantity=11.3):
        """Function to create a harvest object."""
        return Harvest.objects.create(quantity=quantity)

    def test_quantity_creation(self):
        # Test that the object is created properly with only the given data.
        quantity_test_obj = self.create_harvest()
        self.assertTrue(isinstance(quantity_test_obj, Harvest))
        expected_response = "11.3 kilograms"
        self.assertEqual(expected_response, quantity_test_obj.__str__())


class BeeYardAccessTest(TestCase):
    """A class to test the models and views of beeyards including creation and applying
    interventions."""

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
        """A function to test that unauthenticated users cannot see a
        list of beeyards."""
        url = reverse("show_beeyards")
        resp = self.client.get(url)
        # A 401 error is expected without authentication
        self.assertEqual(resp.status_code, 401)

    def test_beeyard_access_authenticated(self):
        """A function to test that an authorized user can access their beeyard information."""
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


class BeeYardActionTest(TestCase):
    """Tests to make sure the action function works."""

    def test_health_check_all(self):
        """Test that a keeper can apply a health check to all hives in a beeyard at once."""

        # Prepare the request by creating and connecting a user
        self.user = User.objects.create_user(username="TestUser2", password="TestPW123")
        self.client = Client()
        request = Mock()
        request.user = self.user
        self.client.force_login(self.user)

        # Make a beeyard and add hives
        test_yard = BeeYard.objects.create(name="TestYard2", beekeeper=self.user)
        for i in range(0, 5):
            Hive.objects.create(
                status="pending",
                species="Buckfast bee",
                beeyard=test_yard,
                queen_year=2022,
                name="Hive_" + str(i),
            )
        yard_id = test_yard.id
        url = f"/beeyards/{yard_id}/health_check_all_hives/"
        # Send a post request with beeyard ID and check the result.
        post_req = self.client.post(url, {})
        self.assertEqual(post_req.status_code, 201)


class TestContaminationCRUD(TestCase):
    """Tests to verify that create, read and delete are correct for contaminatoin data.
    Update test not yet completed."""

    def test_create_contamination(self):
        """Test creating a contamination object via POST request"""
        # Set up a beekeeper object and authenticate
        self.user = User.objects.create_user(username="TestUser2", password="TestPW123")
        self.client = Client()
        request = Mock()
        request.user = self.user
        self.client.force_login(self.user)
        # Create a beeyard and hive
        test_yard = BeeYard.objects.create(name="TestYard2", beekeeper=self.user)
        hive = Hive.objects.create(
            status="active",
            species="Buckfast bee",
            beeyard=test_yard,
            queen_year=2022,
            name="Contaminated",
        )
        # Send a post request and compare it to the expected response.
        data = {"type": "parasite", "hive": hive.id}
        url = f"/contaminations/"
        post_req = self.client.post(url, data)
        self.assertEqual(post_req.status_code, 201)

    def test_read_contamination(self):
        """Test that reading a specified contamination returns the expected result."""
        # Set up a beekeeper object and authenticate
        self.user = User.objects.create_user(username="TestUser3", password="TestPW123")
        self.client = Client()
        request = Mock()
        request.user = self.user
        self.client.force_login(self.user)

        # Create a beeyard and hive
        test_yard = BeeYard.objects.create(name="TestYard3", beekeeper=self.user)
        hive = Hive.objects.create(
            status="active",
            species="Black bee",
            beeyard=test_yard,
            queen_year=2022,
            name="Contaminated 2",
        )

        # Create a contamination object
        contamination = Contamination.objects.create(type="illness", hive=hive)

        # Send a request for the object and compare it to the expected data.
        url = f"/contaminations/{contamination.id}/"
        get_req = self.client.get(url)
        self.assertEqual(get_req.status_code, 200)
        self.assertContains(get_req, "illness")

    def test_delete_contamination(self):
        """Create and remove a test contaminationt to test the delete method."""

        # Set up a beekeeper object and authenticate
        self.user = User.objects.create_user(username="TestUser4", password="TestPW123")
        self.client = Client()
        request = Mock()
        request.user = self.user
        self.client.force_login(self.user)

        # Create a beeyard and hive

        test_yard = BeeYard.objects.create(name="TestYard4", beekeeper=self.user)
        hive = Hive.objects.create(
            status="active",
            species="Black bee",
            beeyard=test_yard,
            queen_year=2022,
            name="Contaminated 2",
        )

        # Create a contamination object.
        contamination = Contamination.objects.create(type="illness", hive=hive)

        # Test that it can be read as expected.
        url = f"/contaminations/{contamination.id}/"
        get_req = self.client.get(url)
        self.assertEqual(get_req.status_code, 200)
        self.assertContains(get_req, "illness")

        # Delete the object
        delete_req = self.client.delete(url)
        # Test that it is successfully deleted.
        self.assertEqual(delete_req.status_code, 204)
