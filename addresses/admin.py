from django.contrib import admin
from .models import Address, NGO, Event
# Register your models here.

admin.site.register(Address)
admin.site.register(NGO)
admin.site.register(Event)