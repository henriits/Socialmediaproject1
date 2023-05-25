from django.contrib import admin
from .models import Profile

# Register your models here

# adding this for User to appear in admin panel
admin.site.register(Profile)