from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index, name="Index"),

    path('login/', views.Login, name="login"),
    path('register/', views.register, name="register"),
    path('user_logout', views.user_logout, name="user_logout"),

    path('forgetpassword', views.forgetpassword, name="forgetpassword"),
    path('checkforgot', views.checkforgot, name="checkforgot"),

    path('create_user/', views.create_user, name="create_user"),
    path('user_login/', views.user_login, name="user_login"),
    path('home/', views.home, name="home"),

    path('details', views.details, name="details"),
    path('profile', views.profile, name="profile"),

    path('checkdetails', views.checkdetails, name="checkdetails"),
    path('showrecords', views.showrecords, name="showrecords"),
    path('checkupload', views.checkupload, name="checkupload"),
    path('report/<str:id>/', views.report, name="report"),

    path('contact_us/', views.contact_us, name="contact_us"),

]
