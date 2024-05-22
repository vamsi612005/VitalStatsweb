from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index, name="Index"),
    path('contact_us/', views.contact_us, name="contact_us"),
    path('login/', views.Login, name="login"),
    path('register/', views.register, name="register"),
    path('create_user/', views.create_user, name="create_user"),
    path('user_login/', views.user_login, name="user_login"),
    path('home/', views.home, name="home"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('details', views.details, name="details"),
    path('profile', views.profile, name="profile"),
    path('checkdetails', views.checkdetails, name="checkdetails"),
    path('upload', views.upload, name="upload"),
    path('checkupload', views.checkupload, name="checkupload"),
]
