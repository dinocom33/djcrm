from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.common.urls')),
    path('profile/', include('apps.userprofile.urls')),
]
