from django.urls import path
from .views import (
    register_view, login_view, logout_view, dashboard_view,
    feedback_view, password_email_view, password_otp_view, 
    password_reset_view, inquiry_view
)

app_name = 'accounts'

urlpatterns = [
    path('dashboard', dashboard_view, name='dashboard'),
    path('feedback', feedback_view, name='feedback'),
    path('inquiry/', inquiry_view, name='inquiry'),
    path('signup', register_view, name='register'),
    path('forgot-password/', password_email_view, name='password-email'),
    path('forgot-password/otp/', password_otp_view, name='password-otp'),
    path('password-reset/', password_reset_view, name='password-reset'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
]
