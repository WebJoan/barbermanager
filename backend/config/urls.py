from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from api.ninja_api import api


urlpatterns = [
    # Django Ninja API
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add admin dashboard only in dev environment
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]