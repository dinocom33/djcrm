from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.lead.models import Lead

User = get_user_model()


class UserFilterList(admin.SimpleListFilter):
    title = 'Created by'
    parameter_name = 'created_by'

    def lookups(self, request, model_admin):
        if request.user.is_superuser and request.user.is_org_owner:
            return (
                (created_by.pk, created_by.email) for created_by in Lead.objects.all()
            )
        else:
            return (
                (created_by.pk, created_by.email) for created_by in
                Lead.objects.filter(organization=request.user.organization)
            )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_by=self.value())
        return queryset


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser and request.user.is_org_owner:
            return Lead.objects.all()

        if request.user.is_org_owner:
            return Lead.objects.filter(
                organization=request.user.organization)

    list_display = ['name', 'email', 'organization', 'team', 'created_by', 'priority', 'status', 'created_at',
                    'updated_at']
    list_filter = ['name', 'email', UserFilterList, 'priority', 'status', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'created_by__email', 'priority', 'status', 'created_at', 'updated_at']
    autocomplete_fields = ['created_by', 'organization', 'team']
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
