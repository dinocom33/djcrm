from django.contrib import admin

from apps.userprofile.models import Userprofile


@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', ]
    list_filter = ['user__username', ]
    search_fields = ['user__username', ]
