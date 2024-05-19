from django.db import models


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


class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    details = models.BooleanField(default=False)

    class Meta:
        db_table = "User_table"

    def __str__(self):
        return self.username


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
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username



