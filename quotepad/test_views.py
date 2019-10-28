from django.test import TestCase

''' Testing functions for views used on the site ''''

class TestViews(TestCase):

    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page,"home.html")

    def test_get_change_password_page(self):
        page = self.client.get("/changepassword/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page,"change_password.html")

    def test_get_file_upload_page(self):
        page = self.client.get("/fileupload/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page,"file_upload.html")

    def test_get_show_uploaded_files_page(self):
        page = self.client.get("/showuploadedfiles/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page,"show_uploaded_files.html")

    def test_get_quote_emailed_page(self):
        page = self.client.get("/quoteemailed/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page,"quote_emailed.html")

    def test_register_page(self):
        page = self.client.get("/register/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page,"register.html")     