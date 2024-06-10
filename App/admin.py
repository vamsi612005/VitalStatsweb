from django.contrib import admin

from .models import ContactUs, Register, Profile, Records

admin.site.register(Profile)
admin.site.register(ContactUs)
admin.site.register(Register)
admin.site.register(Records)
