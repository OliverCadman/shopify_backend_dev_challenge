from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .views import AddProductView

from .test_utils import get_test_form_data

class TestProductViews(TestCase):

    def setUp(self):
        """
        Create a Test User and log them in.
        """
        username = "test user"
        password = "test password"
        email = "test@email.com"

        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email
        )

        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

        self.add_product_url = reverse("add_product")
        self.product_list_url = reverse("product_list")

    def test_get_add_product_view(self):
        """
        Confirm that a GET request to AddProductView returns a 200
        response.
        """
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)
    
    def test_add_product_form_in_add_product_view_context(self):
        """
        Confirm that the form to add a product is present in the
        context for AddProductView.
        """

        response = self.client.get(self.add_product_url)
        self.assertTrue("form" in response.context)

    def test_post_to_add_product_view(self):
        """
        Confirm a successful POST request to Add Product View
        with form to add to ProductForm.
        """

        # Dictionary containing key: value pairs for Product form.
        data = get_test_form_data()
        
        response = self.client.post(self.add_product_url, data, follow=True)
        self.assertRedirects(
            response, self.product_list_url,
            status_code=302, target_status_code=200)
