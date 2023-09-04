from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from djcrm import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.common.urls')),
    path('accounts/', include('apps.account.urls')),
    path('profiles/', include('apps.userprofile.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('leads/', include('apps.lead.urls')),
    path('clients/', include('apps.client.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
