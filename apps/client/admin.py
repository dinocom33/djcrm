from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.client.models import Client

User = get_user_model()


class UserFilterList(admin.SimpleListFilter):
    title = 'Converted by'
    parameter_name = 'converted_by'

    def lookups(self, request, model_admin):
        if not request.user.is_superuser:
            visible_users = model_admin.get_visible_users(request)
            # Sub user - return same group users
            return ((user.id, user) for user in visible_users)
        else:
            # Superuser - return all users
            return ((user.id, user) for user in User.objects.filter())

    def queryset(self, request, queryset):
        return queryset.filter(user=self.value()) if self.value() else queryset


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser and request.user.is_org_owner:
            return Client.objects.all()

        return Client.objects.filter(organization=request.user.organization)

    list_display = ['name', 'email', 'organization', 'team', 'converted_by', 'lead_agent', 'created_at', 'updated_at',
                    'notes']
    list_filter = ['name', 'email', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'converted_by__email', 'priority', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 15
    date_hierarchy = 'created_at'
    autocomplete_fields = ['converted_by', 'organization', 'team', 'lead_agent']

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
