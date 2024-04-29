from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Address)
admin.site.register(ContactMessage)
admin.site.register(WebsiteRating)