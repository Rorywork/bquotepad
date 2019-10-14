from django.contrib import admin

# Register your models here.

from .models import Document, Profile, ProductPrice

admin.site.register(Document)
admin.site.register(Profile)
admin.site.register(ProductPrice)
