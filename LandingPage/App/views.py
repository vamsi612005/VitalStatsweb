from io import BytesIO

import requests
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import ContactUs, Register, Records, Profile
import PIL.Image as Image
import google.generativeai as genai


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


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        if not (email and username and password):
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
                    hash_password = make_password(password)
                    print(hash_password)
                    user = Register.objects.create(username=username, email=email, password=hash_password)
                    user.save()
                    messages.success(request, 'User created successfully. You can now log in.')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return redirect('register')

    return redirect('register')


@csrf_exempt
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
            request.session['username'] = username  # Optionally store the username in session
            # Check if user has additional details and redirect accordingly
            if hasattr(user, 'details') and user.details:
                messages.success(request, 'Login Successfully')
                return redirect('home')
            else:
                return redirect('details')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        messages.error(request, 'Method not allowed.')
        return redirect('login')


@csrf_exempt
@login_required(login_url='/login')
def home(request):
    try:
        user_profile = Profile.objects.get(username=request.user.username)
        profile_image = user_profile.profile_image if user_profile.profile_image else None
        return render(request, "Home.html", {"profile_image": profile_image})
    except Profile.DoesNotExist:
        # Handle case where profile does not exist
        profile_image = None
        return render(request, "Home.html", {"profile_image": profile_image})


@login_required(login_url='/login')
def user_logout(request):
    messages.info(request, "Logout SuccessFully")
    request.session.flush()
    logout(request)
    return redirect('login')


@csrf_exempt
@login_required(login_url='/login')
def details(request):
    username = request.user.username
    data = Register.objects.filter(username=username).first()
    return render(request, "userdetails.html", {'user': data})


@csrf_exempt
@login_required(login_url='/login')
def checkdetails(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        phone_number = request.POST.get('phonenumber')
        nominee_name = request.POST.get('nomineename')
        nominee_phone_number = request.POST.get('nomineephone')
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
            postal_code=postalcode,
            profile_image=profile_image
        )

        if profile_image:
            user_profile.save()
            check = Register.objects.get(email=email)
            check.details = True
            check.save()
            messages.success(request, "Profile Created Successfully")
            return redirect('home')
        else:
            messages.info(request, "Please upload a profile picture")
            return redirect('profile')

    else:
        messages.info(request, "Profile not created")
        return redirect('login')


def profile(request):
    return render(request, "profile.html")


@csrf_exempt
@login_required(login_url='/login')
def showrecords(request):
    if request.user.is_authenticated:
        username = request.session.get('username')
        try:
            user_profile = Profile.objects.get(username=username)
            profile_image = user_profile.profile_image if user_profile.profile_image else None
            records = Records.objects.filter(username=username)
            return render(request, "showrecords.html", {"profile_image": profile_image, "records": records})
        except Profile.DoesNotExist:
            messages.error(request, 'Profile not found.')
            return redirect('home')
        except Records.DoesNotExist:
            messages.error(request, 'No records found.')
            return redirect('home')
    else:
        messages.error(request, 'Login again.')
        return redirect('login')


@csrf_exempt
@login_required(login_url='/login')
def checkupload(request):
    if request.method == "POST":
        username = request.session.get('username')
        file = request.FILES.get('file_name')

        if not file:
            messages.error(request, "No file uploaded")
            return redirect('home')

        valid_image_types = ['image/jpeg', 'image/png', 'image/gif']
        if file.content_type not in valid_image_types:
            messages.error(request, "Please upload a valid image file (JPEG, PNG, GIF).")
            return redirect('home')

        try:
            genai.configure(api_key="AIzaSyBJ8M6eulmKHsYh0o4GP32Ecjcqvsob0gY")
            img = Image.open(file)
            model = genai.GenerativeModel('gemini-pro-vision')
            prompt = "Is it medical data? Yes or No:"
            response_with_prompt = model.generate_content([prompt, img])
            if "yes" in response_with_prompt.text.strip().lower():

                try:
                    record = Records(username=username, health_records=file)
                    record.save()
                    messages.success(request, "File uploaded successfully")
                except ValidationError as e:
                    messages.error(request, f"Error: {str(e)}")
                except Exception as e:
                    messages.error(request, "An error occurred while uploading the file")
            else:
                messages.info(request, "Upload medical data only")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('home')

    messages.error(request, "Invalid request method")
    return redirect('home')


@csrf_exempt
@login_required(login_url='/login')
def report(request, id):
    try:
        record = get_object_or_404(Records, id=id)
        img_url = record.health_records.url
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        genai.configure(api_key="AIzaSyBJ8M6eulmKHsYh0o4GP32Ecjcqvsob0gY")
        model = genai.GenerativeModel('gemini-pro-vision')
        promt = (
            "Please describe  in detail, including its purpose, steps involved, potential risks, and expected outcomes.")
        response = model.generate_content([promt, img])
        generated_text = response.text
        username = request.session.get('username')
        user_profile = Profile.objects.get(username=username)
        profile_image = user_profile.profile_image if user_profile.profile_image else None
        records = Records.objects.filter(username=username)
        return render(request, "showrecords.html",
                      {"profile_image": profile_image, "records": records, "res": generated_text})

    except Exception as e:
        print(f"Error: {e}")
        return redirect('home')


def forgetpassword(request):
    return render(request, "forgetpassword.html")


def checkforgot(request):
    if request.method == "POST":
        username = request.POST.get('username')

        try:
            check = Register.objects.get(username=username)
            return HttpResponse('Username there')
        except Register.DoesNotExist:
            messages.error(request, "Username does not exist")
            return redirect('forgetpassword')
    else:
        return HttpResponse("Invalid request method", status=405)
