from django.shortcuts import render
from properties.models import Property


def index_view(request):
    properties = Property.objects.order_by(
        '-timestamp')[:3]
    context = {
        'properties': properties,
        # 'state_choices': state_choices,
        # 'bedroom_choices': bedroom_choices,
        # 'price_choices': price_choices
    }
    return render(request, 'pages/index.html', context)


def about_view(request):
    return render(request, 'pages/about.html')


def contact_view(request):
    return render(request, 'pages/contact.html')
