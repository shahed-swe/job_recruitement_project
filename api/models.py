from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields.json import DataContains
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=120, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    objects = CustomUserManager()

    def get_full_name(self):
        return self.first_name + ' ' +self.last_name

    def __str__(self):
        return self.email


class Country(models.Model):
    name = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    code = models.CharField(max_length=120)

    class Meta:
        db_table = "country"

    def __str__(self):
        return self.name +' '+self.code

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country")
    name = models.CharField(max_length=120)

    class Meta:
        db_table = "state"

    def __str__(self):
        return self.country.name + ' ' + self.name

class Address(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="stateof")
    name = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    road_number = models.IntegerField()

    class Meta:
        db_table = "address"

    def __str__(self):
        return self.state.country.name + '-> ' + self.state.name+ '-> '+ self.name