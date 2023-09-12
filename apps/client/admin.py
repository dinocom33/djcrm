from django.contrib import admin

from apps.client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser and request.user.is_org_owner:
            return Client.objects.all()

        if request.user.is_org_owner:
            return Client.objects.filter(
                organization=request.user.organization)

    list_display = ['name', 'email', 'organization', 'team', 'converted_by', 'lead_agent', 'created_at', 'updated_at', 'notes']
    list_filter = ['name', 'email', 'converted_by__email', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'converted_by__email', 'priority', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 15
    date_hierarchy = 'created_at'

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
        ('Organization', {
            'fields': [
                'organization',
            ]
        }),
        ('Team', {
            'fields': [
                'team',
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
