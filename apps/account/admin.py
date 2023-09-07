from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from apps.organization.models import Organization

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
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
                "fields": ("email", "password1", "password2", "team", "is_active", "is_agent", "is_org_owner", "is_staff",
                           "is_superuser"
                           ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "get_organization", "team", "date_joined", "last_login", "is_staff",
                    "is_agent", "is_org_owner"
                    )
    list_filter = ("email", "team", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "-is_staff",)
    readonly_fields = ('last_login', 'date_joined')

    def get_organization(self, obj):
        return Organization.objects.filter(members=obj).first()

    get_organization.short_description = 'Organization'

# admin.site.unregister(Group)
