from django.urls import path
from .views import properties_view, property_view, search_view

app_name = 'properties'

urlpatterns = [
    path("", properties_view, name='list'),
    path("<int:property_id>", property_view, name='detail'),
    path("search", search_view, name='search'),
]
