from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import geocoder
# from phonenumber_field.modelfields import PhoneNumberField

access_token = 'pk.eyJ1IjoiazdrYXVzaGFsIiwiYSI6ImNsaDRqZXh4NDBsc3IzaG81NnIwdHpvNGcifQ.Zkv2dg9ykTIQQlkyeyg_HQ'

class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank = True, null = True)
    long = models.FloatField(blank = True, null = True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key = access_token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)
    
class NGO(models.Model):
    ngo_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ngo_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # Contact = models.PhoneNumberField(null=False, blank=False, unique=True)
    Contact = models.CharField(max_length=10, default = "12345678")
    ngolat = models.FloatField(blank = True, null = True)
    ngolong = models.FloatField(blank = True, null = True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.location, key = access_token)
        g = g.latlng
        self.ngolat = g[0]
        self.ngolong = g[1]
        return super(NGO, self).save(*args, **kwargs)
    
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event_attendants = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    event_manager = models.BooleanField(default=True)
    # Contact = models.PhoneNumberField(null=False, blank=False, unique=True)
    Contact = models.CharField(max_length=10, default = "12345678")
    date_posted = models.DateTimeField(default=timezone.now)
    ngolat = models.FloatField(blank = True, null = True)
    ngolong = models.FloatField(blank = True, null = True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.location, key = access_token)
        g = g.latlng
        self.ngolat = g[0]
        self.ngolong = g[1]
        return super(Event, self).save(*args, **kwargs)
