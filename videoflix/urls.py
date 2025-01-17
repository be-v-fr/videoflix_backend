from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users_app.urls')),
    path('api/videos/', include('videos_app.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('docs/', include('docs_app.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if not settings.TESTING:
    urlpatterns += debug_toolbar_urls()
