from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
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
    if request.user.is_authenticated:
        property = get_object_or_404(Property, pk=property_id)
        context = {
            'property': property
        }
        facility = []
        if property.is_school:
            facility.append('School')
        if property.is_firestation:
            facility.append('Fire Station')
        if property.is_policestation:
            facility.append('Police Station')
        if property.is_hospital:
            facility.append('Hospital')
        context['facility'] = ", ".join(facility)
        print(facility)
        return render(request, 'properties/details.html', context)
    messages.warning(request, "You must log in to access our services")
    return redirect('accounts:login')


def search_view(request):
    queryset = Property.objects.order_by('-timestamp')
    values = request.GET
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords and keywords != "":
            queryset = queryset.filter(
                Q(description__icontains=keywords) | Q(zipcode__icontains=keywords))
    # Type
    if 'types' in request.GET:
        types = request.GET['types']
        if types and types != 'All':
            queryset = queryset.filter(type__exact=types)
    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price and price != 'All':
            queryset = queryset.filter(price__lte=price)
    # Area
    if 'area' in request.GET:
        area = request.GET['area']
        if area and area != 'All':
            queryset = queryset.filter(area__exact=area)
    # Status
    if 'status' in request.GET:
        status = request.GET['status']
        if status and status != 'All':
            queryset = queryset.filter(status__exact=status)
    # Verification
    if 'verification' in request.GET:
        verification = request.GET['verification']
        if verification and verification != 'All':
            if verification == "True":
                queryset = queryset.filter(is_verified__exact=True)
            else:
                queryset = queryset.filter(is_verified__exact=False)

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
        'values': values
    }
    return render(request, 'properties/search.html', context)


def add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST.get('School'))
            print(request.FILES)
            title = request.POST.get('title', None)
            address = request.POST.get('address', None)
            zipcode = request.POST.get('zipcode', None)
            area = request.POST.get('area', None)
            types = request.POST.get('types', None)
            status = request.POST.get('status', None)
            sqft = request.POST.get('sqft', None)
            price = request.POST.get('price', None)
            description = request.POST.get('description', None)
            is_school = True if request.POST.get('school', False) else False
            is_firestation = True if request.POST.get(
                'firestation', False) else False
            is_policestation = True if request.POST.get(
                'policestation', False) else False
            is_hospital = True if request.POST.get(
                'hospital', False) else False
            photo_main = request.FILES.get('photo_main', None)
            photo_1 = request.FILES.get('photo_1', None)
            photo_2 = request.FILES.get('photo_2', None)
            photo_3 = request.FILES.get('photo_3', None)
            photo_4 = request.FILES.get('photo_4', None)
            photo_5 = request.FILES.get('photo_5', None)
            if title and address and zipcode and sqft and price and description and photo_main:
                property = Property.objects.create(realtor=request.user, title=title, address=address, zipcode=zipcode, area=area, type=types, status=status, sqft=sqft, price=int(price),
                                                   description=description, photo_main=photo_main, photo_1=photo_1, photo_2=photo_2, photo_3=photo_3, photo_4=photo_4, photo_5=photo_5,
                                                   is_school=is_school, is_firestation=is_firestation, is_policestation=is_policestation, is_hospital=is_hospital)
                property.save()
                messages.success(request, 'Successfully added property')
                return redirect('accounts:dashboard')
            context = {
                'area_choices': area_choices,
                'status_choices': status_choices,
                'type_choices': type_choices,
                'values': request.POST
            }
            messages.error(request, 'Please fill all the required fields')
            return render(request, 'properties/add.html', context)
        context = {
            'area_choices': area_choices,
            'status_choices': status_choices,
            'type_choices': type_choices,
        }
        return render(request, 'properties/add.html', context)
    return redirect('accounts:login')


def delete_view(request, property_id):
    if request.user.is_authenticated:
        property = get_object_or_404(Property, pk=property_id)
        if property.realtor == request.user:
            property.delete()
            messages.success(request, 'Successfully removed property')
            return redirect('accounts:dashboard')
    messages.warning(request, "You must log in to access our services")
    return redirect('accounts:login')
