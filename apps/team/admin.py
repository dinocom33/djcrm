from django.contrib import admin

from apps.team.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'created_by', 'created_at', 'updated_at', 'clients_count']
    list_filter = ['name', 'created_by__email', 'created_at', 'updated_at']
    search_fields = ['name', 'created_by__email', 'created_at', 'updated_at']

    def agents_count(self, obj):
        return obj.members.count()

    agents_count.short_description = 'Agents count'

    def clients_count(self, obj):
        return obj.teams.count()

    clients_count.short_description = 'Clients count'
