import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactUs, Register, Profile


def Index(request):
    return render(request, "Index.html")


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        company = request.POST.get('company')
        message = request.POST.get('message')
        if ContactUs.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('Index')

        if ContactUs.objects.filter(phonenumber=phonenumber).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('Index')

        check = ContactUs(name=name, email=email, phonenumber=phonenumber, company=company, message=message)
        check.save()
        messages.success(request, 'We Will Contact You Soon!')
        return redirect('Index')
    return redirect('Index')


def Login(request):
    return render(request, "Login.html")


def register(request):
    return render(request, "Register.html")


def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (name and email and username and password):
            messages.error(request, 'All fields are required.')
            return redirect('register')
        else:
            if Register.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
            elif Register.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
            else:
                try:
                    password = make_password(password)
                    user = Register.objects.create(name=name, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'User created successfully. You can now log in.')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return redirect('register')

    return redirect('register')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                request.session["username"] = username
                user = Register.objects.get(username=username)
                if check_password(password, user.password):
                    if user.details:
                        return redirect('home')
                    else:
                        return redirect('profile')
            except:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        messages.error(request, 'Method not allowed.')
        return redirect('login')


@login_required
def home(request):
    username =request.session.get('username')
    print(username)
    user_profile = Profile.objects.get(username=username)
    profile_image = user_profile.profile_image if user_profile.profile_image else None
    print(profile_image)
    return render(request, "Home.html", {"img": profile_image})


def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect('login')


def profile(request):
    username = request.session.get('username')
    print(username)
    data = Register.objects.filter(username=username).first()
    return render(request, "profile.html", {'user': data})


def checkdetails(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        phone_number = request.POST.get('phonenumber')
        nominee_name = request.POST.get('nomineename')
        nominee_phone_number = request.POST.get('nomineename')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postalcode = request.POST.get('postalcode')
        profile_image = request.FILES.get('profile_image')
        user_profile = Profile(
            username=username,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            nominee_phone_number=nominee_phone_number,
            nominee_name=nominee_name,
            address=address,
            city=city,
            country=country,
            postal_code=postalcode
        )

        if profile_image:
            # Generate a unique filename using uuid
            unique_filename = str(uuid.uuid4())[:8] + profile_image.name
            user_profile.profile_image.save(unique_filename, profile_image, save=True)

        user_profile.save()

        check = Register.objects.get(email=email)
        check.details = True
        check.save()
        return redirect('home')


def userprofile(request):
    pass
