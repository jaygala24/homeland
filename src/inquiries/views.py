from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from properties.choices import subject_choices

# Create your views here.


def contact_view(request):
    if request.method == "POST":
        print(request.POST)
        if request.user.is_authenticated:
            name = request.user.name
            email = request.user.email
        else:
            name = request.POST.get('fullname', None)
            email = request.POST.get('email', None)
        subject = request.POST.get('subject', None)
        message = request.POST.get('message', None)
        if name and email and subject and message:
            contact = Contact.objects.create(
                name=name, email=email, subject=subject, message=message)
            messages.success(request, 'We will reach out to you soon')
            if request.user.is_authenticated:
                return redirect('accounts:dashboard')
            return redirect('index')
        context = {
            'subject_choices': subject_choices,
            'values': request.POST
        }
        messages.error(request, "Please fill all the required fields")
        return render(request, 'pages/contact.html', context)
    context = {
        'subject_choices': subject_choices,
    }
    return render(request, 'pages/contact.html', context)
