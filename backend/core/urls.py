"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = i18n_patterns(
    path('', lambda request: HttpResponse('', status=302, headers={'Location': '/book/search'})),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('book/', include('book.urls')),
    # If no prefix is given, use the default language
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += path("__reload__/", include("django_browser_reload.urls")),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)