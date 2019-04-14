from django.shortcuts import render, redirect
from properties.models import Property
from properties.choices import (
    price_choices, area_choices, status_choices,
    type_choices, verification_choices
)


def index_view(request):
    properties = Property.objects.order_by(
        '-timestamp')[:3]
    context = {
        'properties': properties,
        'price_choices': price_choices,
        'area_choices': area_choices,
        'status_choices': status_choices,
        'type_choices': type_choices,
        'verification_choices': verification_choices
    }
    return render(request, 'pages/index.html', context)


def about_view(request):
    return render(request, 'pages/about.html')


def contact_view(request):
    return render(request, 'pages/contact.html')


def error_redirect_view(request):
    return redirect('index')


def media_view(request):
    pass
