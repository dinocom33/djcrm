from django.contrib import admin

from apps.organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at', 'updated_at', 'members_count']
    list_filter = ['name', 'owner__email', 'created_at', 'updated_at']
    search_fields = ['name', 'owner__email']

    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = 'Members count'
