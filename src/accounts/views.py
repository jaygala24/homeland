import random
import string
import re
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from properties.models import Property
from inquiries.models import Feedback

User = get_user_model()


def generate_token(stringLength=6):
    """
    Generate a random string of letters and digits
    """
    lettersAndDigits = string.ascii_letters
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


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
            token = generate_token()
            user.token = token + str(user.id)
            user.save()
            subject = 'Account Verification'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email, from_email, ]
            context = {
                'title': 'One Time Password',
                'name': user.name,
                'url': 'http://localhost:8000/user/verify/' + user.token + "/",
                'message': "Verify your email to activate your account"
            }
            message = get_template(
                'accounts/verify_email.html').render(context)
            msg = EmailMessage(subject, message, to=to_list,
                               from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            messages.success(
                request, 'Verify your email to activate your account')
            return redirect('accounts:login')
        # Passwords do not match
        messages.error(request, 'Passwords do not match')
        return redirect('accounts:register')
    return render(request, 'accounts/register.html')


def verify_email_view(request, token):
    user_id = int(re.findall('\d+', token)[0])
    user = User.objects.filter(pk=user_id).first()
    if user.token == token and not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return render(request, 'accounts/login.html')
    return redirect('index')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('accounts:dashboard')
        messages.error(request, 'Invalid credentials')
        return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out')
        return redirect('accounts:login')


def password_email_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get('email', None)
        user = User.objects.filter(email=email).first()
        if user is not None:
            token = generate_token()
            user.token = token + str(user.id)
            user.save()
            subject = 'Password Reset'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email, from_email, ]
            context = {
                'title': 'One Time Password',
                'name': user.name,
                'url': 'http://localhost:8000/user/password-reset/' + user.token + "/",
                'message': "We have received password reset request. Contact customer support if not initiated by you."
            }
            message = get_template(
                'accounts/verify_email.html').render(context)
            msg = EmailMessage(subject, message, to=to_list,
                               from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            messages.success(request, "Email is sent to your registered email")
            return redirect('accounts:password-email')
        messages.error(request, "Invalid email credential")
        return redirect('accounts:password-email')
    return render(request, 'accounts/password_email.html')


def password_reset_view(request, token):
    user_id = int(re.findall('\d+', token)[0])
    user = User.objects.filter(pk=user_id).first()
    if user.token == token:
        if request.method == "POST":
            password = request.POST.get('password', None)
            password2 = request.POST.get('password2', None)
            if password != password2:
                messages.error(request, "Passwords do not match")
                return redirect('accounts:password-reset')
            user.set_password(password)
            user.token = None
            user.save()
            messages.success(request, 'Password Changed Successfully')
            return redirect('accounts:login')
        return render(request, 'accounts/password.html', {'token': token})
    return render(request, 'index')


def dashboard_view(request):
    if request.user.is_authenticated:
        properties_list = Property.objects.order_by(
            '-timestamp').filter(realtor=request.user)
        context = {
            'properties': properties_list
        }
        return render(request, 'accounts/dashboard.html', context)
    return redirect('accounts:login')


def feedback_view(request):
    if request.user.is_authenticated:
        feedback = Feedback.objects.filter(user=request.user).first()
        if request.method == "POST":
            message = request.POST.get('message', None)
            print(message)
            if message != "":
                if feedback is not None:
                    feedback.message = message
                else:
                    feedback = Feedback.objects.create(
                        user=request.user, message=message)
                feedback.save()
                messages.success(request, 'Thanks for your feedback')
                return redirect('accounts:dashboard')
            messages.error(request, 'Please fill the form to submit')
            return redirect('accounts:feedback')
        context = {}
        if feedback is not None:
            context['message'] = feedback.message
        return render(request, 'accounts/feedback.html', context)
    messages.warning(request, "You must log in to access our resources")
    return redirect('login')


def inquiry_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            property_id = request.POST.get('id', None)
            name = request.POST.get('name', None)
            email = request.POST.get('email', None)
            phone = request.POST.get('phone', None)
            if name and email and phone:
                property = get_object_or_404(Property, pk=property_id)
                subject = 'Property Inquiry'
                from_email = settings.EMAIL_HOST_USER
                to_list = [property.realtor.email, from_email, ]
                context = {
                    'title': property.title,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'message': "The following user have showed interest in above mentioned property"
                }
                message = get_template(
                    'accounts/verify_email.html').render(context)
                msg = EmailMessage(subject, message, to=to_list,
                                   from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()
                messages.success(
                    request, 'Thanks for your interest')
                return reverse('properties:detail', {kwargs: {property_id: property_id}})
            return redirect('accounts:dashboard')
    return redirect('accounts:login')
