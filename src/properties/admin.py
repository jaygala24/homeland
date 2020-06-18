from django.contrib import admin
from .models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'realtor', 'is_verified',)
    list_filter = ('is_verified',)
    fieldsets = (
        ('Realtor', {'fields': ('realtor',)}),
        ('Details', {'fields': ('title', 'address',
                                'area', 'city', 'state', 'zipcode', 'type', 'sqft', 'price', 'status', 'description',)}),
        ('Photo', {'fields': ('photo_main', 'photo_1',
                              'photo_2', 'photo_3', 'photo_4', 'photo_5',)}),
        ('Facility', {'fields': ('is_school', 'is_firestation',
                                 'is_policestation', 'is_hospital',)}),
        ('Verification', {'fields': ('is_verified',)}),
    )
    search_fields = ('title', 'zipcode',)
    ordering = ('-timestamp',)
    filter_horizontal = ()


admin.site.register(Property, PropertyAdmin)
