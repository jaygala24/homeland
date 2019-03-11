from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'email', 'phone',)
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        ('Login info', {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('name', 'phone',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2',)}
         ),
    )
    search_fields = ('name',)
    ordering = ('timestamp',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
