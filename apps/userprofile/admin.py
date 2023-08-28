from django.contrib import admin

from apps.userprofile.models import Userprofile


@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', ]
    list_filter = ['user__email', ]
    search_fields = ['user__email', ]
    verbose_name = 'User Profile'
