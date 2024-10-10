from django.contrib import admin
from .models import UserProfile,Review,RSVP,Event
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(RSVP)
admin.site.register(Event)