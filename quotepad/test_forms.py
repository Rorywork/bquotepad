from django.test import TestCase
from django.contrib.auth.models import User
from .models import Document
from .forms import ProductPriceForm, ProfileForm

class TestProductPriceForm(TestCase):

    def test_can_create_a_product_without_an_image(self):
        user = User.objects.first()
        form = ProductPriceForm({'brand':'Test Brand',
                                'model_name':'Test Model',
                                'product_code':'Test Product',
                                'price': 1234,
                                'user': user}, user = user)
        self.assertTrue(form.is_valid())

    def test_can_create_a_product_with_an_image(self):
        user = User.objects.first()
        image = Document.objects.first()
        form = ProductPriceForm({'brand':'Test Brand',
                                'model_name':'Test Model',
                                'product_code':'Test Product',
                                'price': 1234,
                                'user': user,
                                'product_image': image}, user = user)
        self.assertTrue(form.is_valid())

    def test_cannot_create_a_user_profile_with_only_a_name(self):
        user = User.objects.last()
        form = ProfileForm({'first_name':'Test Name 1',
                                'last_name':'Test Name 2',
                                'user': user})
        self.assertFalse(form.is_valid())   