from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.views.static import serve

from r_blog import settings

"""r_blog urls"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('social/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]

if settings.DEBUG:
    urlpatterns.append((path('static/<path:path>', never_cache(serve))))
