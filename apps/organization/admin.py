from django.contrib import admin

from apps.client.models import Client
from apps.lead.models import Lead
from apps.organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at', 'updated_at', 'members_count', 'leads_count', 'clients_count']
    list_filter = ['name', 'owner__email', 'created_at', 'updated_at']
    search_fields = ['name', 'owner__email']

    def members_count(self, obj):
        return obj.members.count()

    members_count.short_description = 'Members count'

    def leads_count(self, obj):
        return Lead.objects.filter(organization=obj).count()

    leads_count.short_description = 'Leads'

    def clients_count(self, obj):
        return Client.objects.filter(organization=obj).count()

    clients_count.short_description = 'Clients'
