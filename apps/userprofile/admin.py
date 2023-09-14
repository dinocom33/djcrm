from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from apps.userprofile.models import Userprofile

User = get_user_model()


@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Userprofile.objects.all()

        if request.user.is_org_owner:
            return Userprofile.objects.filter(
                user__organizations=request.user.organization
            )

    list_display = ['user', 'avatar', ]
    list_filter = ['user__email', ]
    search_fields = ['user__email', ]
    verbose_name = 'User Profile'
    autocomplete_fields = ['user']
