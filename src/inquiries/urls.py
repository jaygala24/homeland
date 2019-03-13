from django.urls import path
from .views import contact_us

app_name = 'inquiries'

urlpatterns = [
    path("", contact_us, name='contact_us'),
]
