from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.team.models import Team

User = get_user_model()


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'created_by', 'created_at', 'updated_at', 'agents_count', 'lead_count', 'clients_count']
    list_filter = ['name', 'created_by__email', 'created_at', 'updated_at']
    search_fields = ['name', 'created_by__email', 'created_at', 'updated_at']
    list_per_page = 15

    def lead_count(self, obj):
        return obj.leads.count()

    lead_count.short_description = 'Leads'

    def clients_count(self, obj):
        return obj.clients.count()

    clients_count.short_description = 'Clients'

    def agents_count(self, obj):
        return obj.agents.count()

    agents_count.short_description = 'Agents'
