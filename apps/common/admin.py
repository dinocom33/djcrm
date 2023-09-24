from django.contrib import admin

from apps.common.models import ContactModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject', 'message']
    search_fields = ['email']
    list_filter = ['email']
    readonly_fields = ['created_at']
