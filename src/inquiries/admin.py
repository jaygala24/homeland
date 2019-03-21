from django.contrib import admin
from .models import Contact, Feedback


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject',)
    list_filter = ('subject',)
    fieldsets = (
        ('User', {'fields': ('name', 'email',)}),
        ('Query', {'fields': ('subject', 'message',)}),
    )
    search_fields = ('name', 'email',)
    ordering = ('-id',)
    filter_horizontal = ()


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fieldsets = (
        ('Feedback', {'fields': ('user', 'message',)}),
    )
    search_fields = ('user',)
    ordering = ('-id',)
    filter_horizontal = ()


admin.site.register(Contact, ContactAdmin)
admin.site.register(Feedback, FeedbackAdmin)
