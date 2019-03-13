from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from properties.models import Property

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        name = first_name + " " + last_name
        # Check for passwords match
        if password == password2:
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Email is already registered')
                return redirect('accounts:register')
            user = User.objects.create_user(
                email=email, name=name, phone=phone, password=password)
            user.save()
            messages.success(
                request, 'Your account has been created and can log in')
            return redirect('accounts:login')
        # Passwords do not match
        messages.error(request, 'Passwords do not match')
        return redirect('accounts:register')
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        # Authenticate
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('accounts:dashboard')
        messages.error(request, 'Invalid credentials')
        return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out')
        return redirect('accounts:login')


def dashboard_view(request):
    if request.user.is_authenticated:
        properties_list = Property.objects.order_by(
            '-timestamp').filter(realtor=request.user)
        context = {
            'properties': properties_list
        }
        return render(request, 'accounts/dashboard.html', context)
    return redirect('accounts:login')
