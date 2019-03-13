from django.urls import path
from .views import properties_view, property_view, search_view, add_view, delete_view

app_name = 'properties'

urlpatterns = [
    path("", properties_view, name='list'),
    path("search", search_view, name='search'),
    path("<int:property_id>", property_view, name='detail'),
    path("<int:property_id>/delete", delete_view, name='delete'),
    path("add", add_view, name='add'),
]
