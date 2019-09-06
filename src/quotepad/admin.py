from django.contrib import admin

# Register your models here.

from .models import Document, Profile

admin.site.register(Document)
admin.site.register(Profile)
