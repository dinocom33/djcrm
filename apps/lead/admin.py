from django.contrib import admin

from apps.lead.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser and request.user.is_org_owner:
            return Lead.objects.all()

        if request.user.is_org_owner:
            return Lead.objects.filter(
                organization=request.user.organization)

    list_display = ['name', 'email', 'organization', 'team', 'created_by', 'priority', 'status', 'created_at', 'updated_at']
    list_filter = ['name', 'email', 'created_by__email', 'priority', 'status', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'created_by__email', 'priority', 'status', 'created_at', 'updated_at']
    autocomplete_fields = ['created_by']
    ordering = ['-created_at']
    list_per_page = 15
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'email',
                'notes',
            )
        }),
        ('Organization', {
            'fields': (
                'organization',
            )
        }),
        (
            'Team', {
                'fields': (
                    'team',
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
        ('Converted', {
            'fields': (
                'converted',
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
