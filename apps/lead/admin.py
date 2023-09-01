from django.contrib import admin

from apps.lead.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_by', 'priority', 'status', 'created_at', 'updated_at']
    list_filter = ['name', 'email', 'created_by__email', 'priority', 'status', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'created_by__email', 'priority', 'status', 'created_at', 'updated_at']
    autocomplete_fields = ['created_by']
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'email',
                'notes',
            )
        }),
        ('Priority', {
            'fields': (
                'priority',
            )
        }),
        ('Status', {
            'fields': (
                'status',
            )
        }),
        ('Created By', {
            'fields': (
                'created_by',
            )
        }),
        ('Important Dates', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )
    readonly_fields = ('created_at', 'updated_at')