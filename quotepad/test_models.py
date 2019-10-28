from django.test import TestCase
from django.contrib.auth.models import User
from .models import Document

''' Testing functions for Models used on the site ''''

class TestDocumentModel(TestCase):

    def test_can_create_a_document_without_an_image(self):
        user = User.objects.first()
        print(user)
        product = Document(user=u"test user",
                            description="test description",
                            document="file path")
        product.save()
        self.assertEqual(product.description, "test description")    