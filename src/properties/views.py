from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property
from .choices import price_choices, area_choices, status_choices, type_choices, verification_choices


def properties_view(request):
    properties_list = Property.objects.order_by('-timestamp')
    # Pagination
    paginator = Paginator(properties_list, 6)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    context = {
        'properties': properties,
        'price_choices': price_choices,
        'area_choices': area_choices,
        'status_choices': status_choices,
        'type_choices': type_choices,
        'verification_choices': verification_choices
    }
    return render(request, 'properties/list.html', context)


def property_view(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    context = {
        'property': property
    }
    return render(request, 'properties/details.html', context)


def search_view(request):
    queryset = Property.objects.order_by('-timestamp')
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset = queryset.filter(
                Q(description__icontains=keywords) | Q(zipcode__icontains=keywords))
    # Type
    if 'type' in request.GET:
        types = request.GET['type']
        if type != 'All':
            queryset = queryset.filter(type__exact=types)
    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price != 'All':
            queryset = queryset.filter(price__exact=price)
    # Area
    if 'area' in request.GET:
        area = request.GET['area']
        if type != 'All':
            queryset = queryset.filter(area__exact=area)
    # Status
    if 'status' in request.GET:
        status = request.GET['status']
        if status != 'All':
            queryset = queryset.filter(status__exact=status)
    # Verification
    if 'verification' in request.GET:
        verification = request.GET['verification']
        if verification != 'All':
            queryset = queryset.filter(is_verified__exact=verification)

    paginator = Paginator(queryset, 6)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    context = {
        'properties': properties,
        'price_choices': price_choices,
        'area_choices': area_choices,
        'status_choices': status_choices,
        'type_choices': type_choices,
        'verification_choices': verification_choices,
        'values': request.GET
    }
    return render(request, 'properties/search.html', context)
