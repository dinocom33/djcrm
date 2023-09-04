from django.contrib import admin

from apps.client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'converted_by', 'lead_agent', 'created_at', 'updated_at', 'notes']
    list_filter = ['name', 'email', 'converted_by__email', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'converted_by__email', 'priority', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Personal information', {
            'fields': [
                'name',
                'email',
            ],
        }),
        ('Notes', {
            'fields': [
                'notes',
            ]
        }),
        ('Converted by', {
            'fields': [
                'converted_by',
                'lead_agent',
            ]
        }),
        ('Important dates', {
            'fields': [
                'created_at',
                'updated_at',
            ]
        }),
    ]
