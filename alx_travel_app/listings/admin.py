from django.contrib import admin

from .models import User, Listing, Booking, Review, Message, Payment

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(Payment)
