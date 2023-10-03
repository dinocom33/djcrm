from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from apps.client.models import Client
from apps.lead.models import Lead
from apps.organization.models import Organization

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser and request.user.is_org_owner:
            return User.objects.all()

        if request.user.is_org_owner:
            return User.objects.filter(
                organizations=request.user.organization,
            )

    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Team"), {"fields": ("team",)}),
        (_("Permissions"),
         {
             "fields": (
                 "is_active",
                 "is_agent",
                 "is_org_owner",
                 "is_staff",
                 "is_superuser",
                 "groups",
                 "user_permissions",
             ),
         },
         ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email", "password1", "password2", "team", "is_active", "is_agent", "is_org_owner", "is_staff",
                    "is_superuser"
                ),
            },
        ),
    )
    list_display = (
        "email", "first_name", "last_name", "get_organization", "team", "date_joined", "last_login", "is_superuser", "is_staff",
        "is_agent", "is_org_owner", "leads_per_agent_count", "clients_per_agent_count"
    )
    list_filter = ("email", "team", "is_agent", "is_org_owner", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name", "team")
    ordering = ("email", "-is_staff",)
    list_per_page = 15
    readonly_fields = ('last_login', 'date_joined')
    autocomplete_fields = ['team']

    def get_organization(self, obj):
        return Organization.objects.filter(members=obj).first()

    get_organization.short_description = 'Organization'

    def leads_per_agent_count(self, obj):
        return Lead.objects.filter(created_by=obj).count()

    leads_per_agent_count.short_description = 'Leads'

    def clients_per_agent_count(self, obj):
        return Client.objects.filter(converted_by=obj).count()

    clients_per_agent_count.short_description = 'Clients'
