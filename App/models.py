import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, unique=True)
    phonenumber = models.CharField(max_length=20, unique=True, blank=False)
    company = models.CharField(max_length=100, blank=False)
    message = models.TextField(blank=False)

    class Meta:
        db_table = "Contactus_table"

    def __str__(self):
        return self.name


class Register(AbstractUser):
    details = models.BooleanField(default=False)

    class Meta:
        db_table = "User_table"


class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nominee_name = models.CharField(max_length=255, blank=True, null=True)
    nominee_phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    profile_image = CloudinaryField('image')

    def __str__(self):
        return self.username


class Records(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=55, blank=False)
    health_records = CloudinaryField('image')
    uploadtime = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.username
